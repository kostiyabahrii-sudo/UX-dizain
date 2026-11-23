package store

import (
	"context"
	"time"

	"github.com/jackc/pgx/v5"

	"fitkit/api/internal/domain"
)

// ---------- employees & sessions

type EmployeeAuth struct {
	domain.Employee
	PasswordHash string
}

func (q *Q) CreateEmployee(ctx context.Context, name, email string, role domain.Role, hash string) (domain.Employee, error) {
	e := domain.Employee{Name: name, Email: email, Role: role}
	err := q.db.QueryRow(ctx, `INSERT INTO employees (name, email, role, password_hash) VALUES ($1, lower($2), $3, $4) RETURNING id`, name, email, role, hash).Scan(&e.ID)
	return e, err
}

func (q *Q) EmployeeByEmail(ctx context.Context, email string) (EmployeeAuth, error) {
	var e EmployeeAuth
	err := q.db.QueryRow(ctx, `SELECT id, name, email, role, password_hash FROM employees WHERE email = lower($1)`, email).Scan(&e.ID, &e.Name, &e.Email, &e.Role, &e.PasswordHash)
	return e, notFound(err)
}

func (q *Q) Employees(ctx context.Context) ([]domain.Employee, error) {
	rows, err := q.db.Query(ctx, `SELECT id, name, email, role FROM employees ORDER BY name`)
	if err != nil {
		return nil, err
	}
	return pgx.CollectRows(rows, func(r pgx.CollectableRow) (domain.Employee, error) {
		var e domain.Employee
		err := r.Scan(&e.ID, &e.Name, &e.Email, &e.Role)
		return e, err
	})
}

func (q *Q) CreateSession(ctx context.Context, tokenHash []byte, employeeID string, expires time.Time) error {
	_, err := q.db.Exec(ctx, `INSERT INTO sessions (token_hash, employee_id, expires_at) VALUES ($1, $2, $3)`, tokenHash, employeeID, expires)
	return err
}

func (q *Q) SessionEmployee(ctx context.Context, tokenHash []byte) (domain.Employee, error) {
	var e domain.Employee
	err := q.db.QueryRow(ctx, `SELECT e.id, e.name, e.email, e.role FROM sessions s JOIN employees e ON e.id = s.employee_id WHERE s.token_hash = $1 AND s.expires_at > now()`, tokenHash).Scan(&e.ID, &e.Name, &e.Email, &e.Role)
	return e, notFound(err)
}

func (q *Q) DeleteSession(ctx context.Context, tokenHash []byte) error {
	_, err := q.db.Exec(ctx, `DELETE FROM sessions WHERE token_hash = $1`, tokenHash)
	return err
}

// ---------- clients

const clientCols = `id, name, phone, telegram, city, branch, sizes, stores, dislikes, note`

func scanClient(r pgx.Row) (domain.Client, error) {
	var c domain.Client
	err := r.Scan(&c.ID, &c.Name, &c.Phone, &c.Telegram, &c.City, &c.Branch, &c.Sizes, &c.Stores, &c.Dislikes, &c.Note)
	return c, err
}

func (q *Q) Clients(ctx context.Context) ([]domain.Client, error) {
	rows, err := q.db.Query(ctx, `SELECT `+clientCols+` FROM clients ORDER BY name`)
	if err != nil {
		return nil, err
	}
	return pgx.CollectRows(rows, func(r pgx.CollectableRow) (domain.Client, error) { return scanClient(r) })
}

func (q *Q) Client(ctx context.Context, id string) (domain.Client, error) {
	c, err := scanClient(q.db.QueryRow(ctx, `SELECT `+clientCols+` FROM clients WHERE id = $1`, id))
	return c, notFound(err)
}

// UpsertClient creates or updates a client by its id in the Fitkit client app.
func (q *Q) UpsertClient(ctx context.Context, externalID string, c domain.Client) (string, error) {
	var id string
	err := q.db.QueryRow(ctx, `
		INSERT INTO clients (external_id, name, phone, telegram, city, branch, sizes, stores, dislikes, note)
		VALUES (NULLIF($1, ''), $2, $3, $4, $5, $6, $7, $8, $9, $10)
		ON CONFLICT (external_id) DO UPDATE SET name = EXCLUDED.name, phone = EXCLUDED.phone, telegram = EXCLUDED.telegram,
			city = EXCLUDED.city, branch = EXCLUDED.branch, sizes = EXCLUDED.sizes, stores = EXCLUDED.stores
		RETURNING id`,
		externalID, c.Name, c.Phone, c.Telegram, c.City, c.Branch, c.Sizes, c.Stores, c.Dislikes, c.Note).Scan(&id)
	return id, err
}

func (q *Q) ClientIDByExternal(ctx context.Context, externalID string) (string, error) {
	var id string
	err := q.db.QueryRow(ctx, `SELECT id FROM clients WHERE external_id = $1`, externalID).Scan(&id)
	return id, notFound(err)
}

// ---------- orders

type NewOrder struct {
	Number     string // empty → next from order_number_seq
	ExternalID string
	ClientID   string
	OwnerID    *string
	Status     domain.OrderStatus
	Paid       *domain.Money
	Fee        domain.Money
	Problem    *string
	Location   *string
	CreatedAt  time.Time
	DueAt      time.Time
	Items      []domain.Item
}

func (q *Q) InsertOrder(ctx context.Context, o NewOrder) (string, string, error) {
	var id, number string
	err := q.db.QueryRow(ctx, `
		INSERT INTO orders (number, external_id, client_id, owner_id, status, paid, fee, problem, location, created_at, due_at, updated_at)
		VALUES (COALESCE(NULLIF($11, ''), '#' || lpad(nextval('order_number_seq')::text, 4, '0')), NULLIF($1, ''), $2, $3, $4, $5, $6, $7, $8, $9, $10, $9)
		RETURNING id, number`,
		o.ExternalID, o.ClientID, o.OwnerID, o.Status, o.Paid, o.Fee, o.Problem, o.Location, o.CreatedAt, o.DueAt, o.Number).Scan(&id, &number)
	if err != nil {
		return "", "", err
	}
	for i, it := range o.Items {
		if _, err := q.db.Exec(ctx, `
			INSERT INTO items (order_id, position, photo, name, store, url, size, qty, price, store_price, comment, status, confirm_sent_at)
			VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)`,
			id, i, it.Photo, it.Name, it.Store, it.URL, it.Size, it.Qty, it.Price, it.StorePrice, it.Comment, it.Status, it.ConfirmSentAt); err != nil {
			return "", "", err
		}
	}
	return id, number, nil
}

const orderCols = `id, number, client_id, owner_id, status, paid, fee, problem, location, created_at, due_at`

func scanOrder(r pgx.Row) (domain.Order, error) {
	var o domain.Order
	err := r.Scan(&o.ID, &o.Number, &o.ClientID, &o.OwnerID, &o.Status, &o.Paid, &o.Fee, &o.Problem, &o.Location, &o.CreatedAt, &o.DueAt)
	return o, err
}

type OrderFilter struct {
	Statuses []domain.OrderStatus
	OwnerID  string
	ClientID string
	IDs      []string
}

// Orders lists orders with items, notes and history.
func (q *Q) Orders(ctx context.Context, f OrderFilter) ([]domain.Order, error) {
	sql := `SELECT ` + orderCols + ` FROM orders WHERE true`
	var args []any
	add := func(cond string, v any) {
		args = append(args, v)
		sql += " AND " + cond + "$" + itoa(len(args))
	}
	if len(f.Statuses) > 0 {
		ss := make([]string, len(f.Statuses))
		for i, s := range f.Statuses {
			ss[i] = string(s)
		}
		add("status = ANY(", ss)
		sql += ")"
	}
	if f.OwnerID != "" {
		add("owner_id = ", f.OwnerID)
	}
	if f.ClientID != "" {
		add("client_id = ", f.ClientID)
	}
	if len(f.IDs) > 0 {
		add("id = ANY(", f.IDs)
		sql += "::uuid[])"
	}
	sql += ` ORDER BY due_at`
	rows, err := q.db.Query(ctx, sql, args...)
	if err != nil {
		return nil, err
	}
	orders, err := pgx.CollectRows(rows, func(r pgx.CollectableRow) (domain.Order, error) { return scanOrder(r) })
	if err != nil {
		return nil, err
	}
	return orders, q.loadChildren(ctx, orders)
}

// Order loads one order; lock = SELECT … FOR UPDATE (use inside Tx).
func (q *Q) Order(ctx context.Context, id string, lock bool) (domain.Order, error) {
	sql := `SELECT ` + orderCols + ` FROM orders WHERE id = $1`
	if lock {
		sql += ` FOR UPDATE`
	}
	o, err := scanOrder(q.db.QueryRow(ctx, sql, id))
	if err != nil {
		return o, notFound(err)
	}
	list := []domain.Order{o}
	err = q.loadChildren(ctx, list)
	return list[0], err
}

func (q *Q) OrderIDByExternal(ctx context.Context, externalID string) (string, error) {
	var id string
	err := q.db.QueryRow(ctx, `SELECT id FROM orders WHERE external_id = $1`, externalID).Scan(&id)
	return id, notFound(err)
}

func (q *Q) loadChildren(ctx context.Context, orders []domain.Order) error {
	if len(orders) == 0 {
		return nil
	}
	ids := make([]string, len(orders))
	idx := make(map[string]int, len(orders))
	for i, o := range orders {
		ids[i] = o.ID
		idx[o.ID] = i
		orders[i].Items, orders[i].Notes, orders[i].History = []domain.Item{}, []domain.Note{}, []domain.HistoryEvent{}
	}
	rows, err := q.db.Query(ctx, `SELECT order_id, id, photo, name, store, url, size, qty, price, store_price, comment, status, confirm_sent_at FROM items WHERE order_id = ANY($1::uuid[]) ORDER BY position`, ids)
	if err != nil {
		return err
	}
	for rows.Next() {
		var oid string
		var it domain.Item
		if err := rows.Scan(&oid, &it.ID, &it.Photo, &it.Name, &it.Store, &it.URL, &it.Size, &it.Qty, &it.Price, &it.StorePrice, &it.Comment, &it.Status, &it.ConfirmSentAt); err != nil {
			rows.Close()
			return err
		}
		orders[idx[oid]].Items = append(orders[idx[oid]].Items, it)
	}
	rows.Close()
	if err := rows.Err(); err != nil {
		return err
	}
	rows, err = q.db.Query(ctx, `SELECT order_id, id, author, created_at, text FROM notes WHERE order_id = ANY($1::uuid[]) ORDER BY created_at`, ids)
	if err != nil {
		return err
	}
	for rows.Next() {
		var oid string
		var n domain.Note
		if err := rows.Scan(&oid, &n.ID, &n.Author, &n.At, &n.Text); err != nil {
			rows.Close()
			return err
		}
		orders[idx[oid]].Notes = append(orders[idx[oid]].Notes, n)
	}
	rows.Close()
	if err := rows.Err(); err != nil {
		return err
	}
	rows, err = q.db.Query(ctx, `SELECT order_id, at, who, what FROM history WHERE order_id = ANY($1::uuid[]) ORDER BY at, id`, ids)
	if err != nil {
		return err
	}
	for rows.Next() {
		var oid string
		var h domain.HistoryEvent
		if err := rows.Scan(&oid, &h.At, &h.Who, &h.What); err != nil {
			rows.Close()
			return err
		}
		orders[idx[oid]].History = append(orders[idx[oid]].History, h)
	}
	rows.Close()
	return rows.Err()
}

// TakeOrder assigns a new, unassigned order atomically. ok=false if someone was faster.
func (q *Q) TakeOrder(ctx context.Context, id, employeeID string, due time.Time) (bool, error) {
	tag, err := q.db.Exec(ctx, `UPDATE orders SET owner_id = $2, status = 'in_progress', due_at = $3, updated_at = now() WHERE id = $1 AND status = 'new' AND owner_id IS NULL`, id, employeeID, due)
	return tag.RowsAffected() == 1, err
}

// OldestNewOrder returns the id of the oldest unassigned request, locked with SKIP LOCKED.
func (q *Q) OldestNewOrder(ctx context.Context) (string, error) {
	var id string
	err := q.db.QueryRow(ctx, `SELECT id FROM orders WHERE status = 'new' AND owner_id IS NULL ORDER BY created_at LIMIT 1 FOR UPDATE SKIP LOCKED`).Scan(&id)
	return id, notFound(err)
}

// SaveOrder writes the mutable order fields.
func (q *Q) SaveOrder(ctx context.Context, o domain.Order) error {
	_, err := q.db.Exec(ctx, `UPDATE orders SET owner_id = $2, status = $3, problem = $4, location = $5, due_at = $6, updated_at = now() WHERE id = $1`,
		o.ID, o.OwnerID, o.Status, o.Problem, o.Location, o.DueAt)
	return err
}

func (q *Q) SaveItem(ctx context.Context, it domain.Item) error {
	_, err := q.db.Exec(ctx, `UPDATE items SET price = $2, store_price = $3, status = $4, confirm_sent_at = $5 WHERE id = $1`,
		it.ID, it.Price, it.StorePrice, it.Status, it.ConfirmSentAt)
	return err
}

func (q *Q) AddHistory(ctx context.Context, orderID, who, what string) error {
	_, err := q.db.Exec(ctx, `INSERT INTO history (order_id, who, what) VALUES ($1, $2, $3)`, orderID, who, what)
	return err
}

func (q *Q) AddHistoryAt(ctx context.Context, orderID, who, what string, at time.Time) error {
	_, err := q.db.Exec(ctx, `INSERT INTO history (order_id, who, what, at) VALUES ($1, $2, $3, $4)`, orderID, who, what, at)
	return err
}

func (q *Q) AddNote(ctx context.Context, orderID string, authorID *string, author, text string, at time.Time) (domain.Note, error) {
	n := domain.Note{Author: author, Text: text, At: at}
	err := q.db.QueryRow(ctx, `INSERT INTO notes (order_id, author_id, author, text, created_at) VALUES ($1, $2, $3, $4, $5) RETURNING id`, orderID, authorID, author, text, at).Scan(&n.ID)
	return n, err
}

// AwaitingExpired lists (order id, item id) of price confirmations older than cutoff.
func (q *Q) AwaitingExpired(ctx context.Context, cutoff time.Time) ([][2]string, error) {
	rows, err := q.db.Query(ctx, `SELECT order_id, id FROM items WHERE status = 'awaiting' AND confirm_sent_at < $1`, cutoff)
	if err != nil {
		return nil, err
	}
	return pgx.CollectRows(rows, func(r pgx.CollectableRow) ([2]string, error) {
		var p [2]string
		err := r.Scan(&p[0], &p[1])
		return p, err
	})
}

// ---------- shipments

const shipmentCols = `id, order_id, leg, store, carrier, tracking, source, problem, at_warehouse, delivered, created_at`

func scanShipment(r pgx.Row) (domain.Shipment, error) {
	var s domain.Shipment
	err := r.Scan(&s.ID, &s.OrderID, &s.Leg, &s.Store, &s.Carrier, &s.Tracking, &s.Source, &s.Problem, &s.AtWarehouse, &s.Delivered, &s.CreatedAt)
	return s, err
}

func (q *Q) Shipments(ctx context.Context, orderID string) ([]domain.Shipment, error) {
	sql := `SELECT ` + shipmentCols + ` FROM shipments`
	var args []any
	if orderID != "" {
		sql += ` WHERE order_id = $1`
		args = append(args, orderID)
	}
	sql += ` ORDER BY created_at`
	rows, err := q.db.Query(ctx, sql, args...)
	if err != nil {
		return nil, err
	}
	list, err := pgx.CollectRows(rows, func(r pgx.CollectableRow) (domain.Shipment, error) { return scanShipment(r) })
	if err != nil || len(list) == 0 {
		return list, err
	}
	ids := make([]string, len(list))
	idx := map[string]int{}
	for i, s := range list {
		ids[i] = s.ID
		idx[s.ID] = i
		list[i].Events = []domain.TrackingEvent{}
	}
	rows, err = q.db.Query(ctx, `SELECT shipment_id, at, title, detail FROM tracking_events WHERE shipment_id = ANY($1::uuid[]) ORDER BY at, id`, ids)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var sid string
		var e domain.TrackingEvent
		if err := rows.Scan(&sid, &e.At, &e.Title, &e.Detail); err != nil {
			return nil, err
		}
		list[idx[sid]].Events = append(list[idx[sid]].Events, e)
	}
	return list, rows.Err()
}

func (q *Q) Shipment(ctx context.Context, id string) (domain.Shipment, error) {
	s, err := scanShipment(q.db.QueryRow(ctx, `SELECT `+shipmentCols+` FROM shipments WHERE id = $1 FOR UPDATE`, id))
	return s, notFound(err)
}

func (q *Q) ShipmentByTracking(ctx context.Context, tracking string) (domain.Shipment, error) {
	s, err := scanShipment(q.db.QueryRow(ctx, `SELECT `+shipmentCols+` FROM shipments WHERE replace(tracking, ' ', '') = replace($1, ' ', '') FOR UPDATE`, tracking))
	return s, notFound(err)
}

func (q *Q) InsertShipment(ctx context.Context, s domain.Shipment) (string, error) {
	var id string
	created := s.CreatedAt
	if created.IsZero() {
		created = time.Now()
	}
	err := q.db.QueryRow(ctx, `INSERT INTO shipments (order_id, leg, store, carrier, tracking, source, problem, at_warehouse, delivered, created_at) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) RETURNING id`,
		s.OrderID, s.Leg, s.Store, s.Carrier, s.Tracking, s.Source, s.Problem, s.AtWarehouse, s.Delivered, created).Scan(&id)
	return id, err
}

func (q *Q) SaveShipment(ctx context.Context, s domain.Shipment) error {
	_, err := q.db.Exec(ctx, `UPDATE shipments SET carrier = $2, tracking = $3, source = $4, problem = $5, at_warehouse = $6, delivered = $7 WHERE id = $1`,
		s.ID, s.Carrier, s.Tracking, s.Source, s.Problem, s.AtWarehouse, s.Delivered)
	return err
}

func (q *Q) AddTrackingEvent(ctx context.Context, shipmentID string, e domain.TrackingEvent) error {
	if e.At.IsZero() {
		e.At = time.Now()
	}
	_, err := q.db.Exec(ctx, `INSERT INTO tracking_events (shipment_id, at, title, detail) VALUES ($1, $2, $3, $4)`, shipmentID, e.At, e.Title, e.Detail)
	return err
}

// StalledInbound returns store→warehouse parcels to flag: no tracking after noTrackingCutoff,
// or no tracking event since noMoveCutoff. Already-flagged parcels are skipped.
func (q *Q) StalledInbound(ctx context.Context, noTrackingCutoff, noMoveCutoff time.Time) (noTracking, noMove []string, err error) {
	rows, err := q.db.Query(ctx, `
		SELECT s.id, s.tracking IS NULL
		FROM shipments s
		WHERE s.leg = 'in' AND NOT s.at_warehouse AND s.problem IS NULL AND (
			(s.tracking IS NULL AND s.created_at < $1) OR
			(s.tracking IS NOT NULL AND COALESCE((SELECT max(at) FROM tracking_events e WHERE e.shipment_id = s.id), s.created_at) < $2))`,
		noTrackingCutoff, noMoveCutoff)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var id string
		var missing bool
		if err := rows.Scan(&id, &missing); err != nil {
			return nil, nil, err
		}
		if missing {
			noTracking = append(noTracking, id)
		} else {
			noMove = append(noMove, id)
		}
	}
	return noTracking, noMove, rows.Err()
}

// ---------- tickets

func (q *Q) Tickets(ctx context.Context, status string) ([]domain.Ticket, error) {
	sql := `SELECT id, client_id, order_id, status, summary, updated_at FROM tickets`
	var args []any
	if status != "" {
		sql += ` WHERE status = $1`
		args = append(args, status)
	}
	sql += ` ORDER BY updated_at DESC`
	rows, err := q.db.Query(ctx, sql, args...)
	if err != nil {
		return nil, err
	}
	list, err := pgx.CollectRows(rows, func(r pgx.CollectableRow) (domain.Ticket, error) {
		var t domain.Ticket
		err := r.Scan(&t.ID, &t.ClientID, &t.OrderID, &t.Status, &t.Summary, &t.UpdatedAt)
		t.Messages = []domain.Message{}
		return t, err
	})
	if err != nil || len(list) == 0 {
		return list, err
	}
	ids := make([]string, len(list))
	idx := map[string]int{}
	for i, t := range list {
		ids[i] = t.ID
		idx[t.ID] = i
	}
	rows, err = q.db.Query(ctx, `SELECT ticket_id, id, sender, text, at FROM messages WHERE ticket_id = ANY($1::uuid[]) ORDER BY at, id`, ids)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var tid string
		var m domain.Message
		if err := rows.Scan(&tid, &m.ID, &m.From, &m.Text, &m.At); err != nil {
			return nil, err
		}
		list[idx[tid]].Messages = append(list[idx[tid]].Messages, m)
	}
	return list, rows.Err()
}

func (q *Q) Ticket(ctx context.Context, id string) (domain.Ticket, error) {
	var t domain.Ticket
	err := q.db.QueryRow(ctx, `SELECT id, client_id, order_id, status, summary, updated_at FROM tickets WHERE id = $1 FOR UPDATE`, id).Scan(&t.ID, &t.ClientID, &t.OrderID, &t.Status, &t.Summary, &t.UpdatedAt)
	return t, notFound(err)
}

// OpenTicketFor returns the open ticket of a client for an order, if any.
func (q *Q) OpenTicketFor(ctx context.Context, clientID string, orderID *string) (string, error) {
	var id string
	err := q.db.QueryRow(ctx, `SELECT id FROM tickets WHERE client_id = $1 AND status = 'open' AND order_id IS NOT DISTINCT FROM $2 ORDER BY updated_at DESC LIMIT 1`, clientID, orderID).Scan(&id)
	return id, notFound(err)
}

func (q *Q) InsertTicket(ctx context.Context, t domain.Ticket) (string, error) {
	var id string
	at := t.UpdatedAt
	if at.IsZero() {
		at = time.Now()
	}
	err := q.db.QueryRow(ctx, `INSERT INTO tickets (client_id, order_id, status, summary, updated_at) VALUES ($1, $2, $3, $4, $5) RETURNING id`, t.ClientID, t.OrderID, t.Status, t.Summary, at).Scan(&id)
	return id, err
}

func (q *Q) AddMessage(ctx context.Context, ticketID, sender string, authorID *string, text string, at time.Time) (domain.Message, error) {
	m := domain.Message{From: sender, Text: text, At: at}
	if err := q.db.QueryRow(ctx, `INSERT INTO messages (ticket_id, sender, author_id, text, at) VALUES ($1, $2, $3, $4, $5) RETURNING id`, ticketID, sender, authorID, text, at).Scan(&m.ID); err != nil {
		return m, err
	}
	_, err := q.db.Exec(ctx, `UPDATE tickets SET updated_at = GREATEST(updated_at, $2) WHERE id = $1`, ticketID, at)
	return m, err
}

func (q *Q) SetTicket(ctx context.Context, id, status, summary string) error {
	_, err := q.db.Exec(ctx, `UPDATE tickets SET status = $2, summary = $3, updated_at = now() WHERE id = $1`, id, status, summary)
	return err
}

func itoa(i int) string {
	const digits = "0123456789"
	if i < 10 {
		return string(digits[i])
	}
	return itoa(i/10) + string(digits[i%10])
}
