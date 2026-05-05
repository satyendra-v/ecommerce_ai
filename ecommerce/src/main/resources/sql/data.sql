use ecommercedb;

-- customers (20 rows)
INSERT INTO customer (customer_id, name, email, address) VALUES
(1, 'John Doe', 'john.doe@example.com', '123 Maple St, Springfield, IL 62704'),
(2, 'Jane Smith', 'jane.smith@example.com', '456 Oak Ave, Seattle, WA 98101'),
(3, 'Michael Johnson', 'michael.johnson@example.com', '789 Pine Rd, Austin, TX 73301'),
(4, 'Emily Davis', 'emily.davis@example.com', '321 Cedar Ln, Denver, CO 80203'),
(5, 'Robert Brown', 'robert.brown@example.com', '654 Birch Blvd, Miami, FL 33101'),
(6, 'Linda Wilson', 'linda.wilson@example.com', '987 Aspen Way, Portland, OR 97205'),
(7, 'David Miller', 'david.miller@example.com', '159 Walnut St, Boston, MA 02110'),
(8, 'Sarah Lee', 'sarah.lee@example.com', '753 Cherry Ct, San Francisco, CA 94102'),
(9, 'James Anderson', 'james.anderson@example.com', '852 Spruce Dr, Chicago, IL 60605'),
(10, 'Patricia Taylor', 'patricia.taylor@example.com', '951 Poplar Pl, New York, NY 10001'),
(11, 'Charles Thomas', 'charles.thomas@example.com', '147 Elm St, Philadelphia, PA 19103'),
(12, 'Barbara Jackson', 'barbara.jackson@example.com', '258 Willow Rd, Atlanta, GA 30303'),
(13, 'Christopher White', 'christopher.white@example.com', '369 Magnolia Ave, Dallas, TX 75201'),
(14, 'Karen Harris', 'karen.harris@example.com', '420 Hickory St, San Diego, CA 92101'),
(15, 'Matthew Martin', 'matthew.martin@example.com', '531 Fir Ln, Columbus, OH 43004'),
(16, 'Nancy Thompson', 'nancy.thompson@example.com', '642 Palm St, Phoenix, AZ 85001'),
(17, 'Anthony Garcia', 'anthony.garcia@example.com', '753 Olive Rd, Las Vegas, NV 89109'),
(18, 'Lisa Martinez', 'lisa.martinez@example.com', '864 Maplewood Dr, Charlotte, NC 28202'),
(19, 'Mark Robinson', 'mark.robinson@example.com', '975 Sycamore Ave, Indianapolis, IN 46204'),
(20, 'Susan Clark', 'susan.clark@example.com', '186 Riverbend Ln, Minneapolis, MN 55401');

-- products (20 rows)
INSERT INTO product (product_id, name, description, price, sku, created_at, updated_at) VALUES
(1, 'Everyday Water Bottle', 'Stainless steel, 750ml, double-wall insulated', 19.99, 'PROD-1001', '2024-06-01 09:00:00', '2024-06-01 09:00:00'),
(2, 'Wireless Earbuds', 'Bluetooth 5.2, noise reduction, 24h battery', 49.50, 'PROD-1002', '2024-07-15 11:30:00', '2024-07-15 11:30:00'),
(3, 'Travel Adapter', 'Universal adapter with USB-C and USB-A ports', 5.99, 'PROD-1003', '2024-08-05 14:20:00', '2024-08-05 14:20:00'),
(4, 'Desk Lamp', 'LED desk lamp with adjustable brightness', 129.00, 'PROD-1004', '2024-09-10 10:00:00', '2024-09-10 10:00:00'),
(5, 'Coffee Mug', 'Ceramic, 350ml, dishwasher safe', 9.95, 'PROD-1005', '2024-10-01 08:45:00', '2024-10-01 08:45:00'),
(6, 'Gaming Keyboard', 'Mechanical keyboard with RGB backlight', 249.99, 'PROD-1006', '2024-11-12 16:10:00', '2024-11-12 16:10:00'),
(7, 'Phone Case', 'Shockproof TPU, compatible with popular models', 14.49, 'PROD-1007', '2024-12-03 12:00:00', '2024-12-03 12:00:00'),
(8, 'Bluetooth Speaker', 'Portable speaker, IPX5, 12h playtime', 79.00, 'PROD-1008', '2025-01-08 09:30:00', '2025-01-08 09:30:00'),
(9, '4K Monitor', '27-inch 4K UHD, IPS, 60Hz', 299.00, 'PROD-1009', '2025-02-20 13:00:00', '2025-02-20 13:00:00'),
(10, 'Sticker Pack', 'Assorted vinyl stickers, 20 pcs', 2.99, 'PROD-1010', '2025-02-28 15:00:00', '2025-02-28 15:00:00'),
(11, 'Notebook', 'A5 hardbound notebook, 200 pages', 15.00, 'PROD-1011', '2025-03-05 10:15:00', '2025-03-05 10:15:00'),
(12, 'Yoga Mat', 'Non-slip, 6mm thickness', 39.95, 'PROD-1012', '2025-03-20 07:50:00', '2025-03-20 07:50:00'),
(13, 'Keychain', 'Minimal leather keychain', 7.50, 'PROD-1013', '2025-04-01 11:00:00', '2025-04-01 11:00:00'),
(14, 'Smartwatch', 'Fitness tracking, heart-rate monitor', 199.99, 'PROD-1014', '2025-04-15 18:30:00', '2025-04-15 18:30:00'),
(15, 'Wireless Charger', 'Qi fast charger, 15W', 24.00, 'PROD-1015', '2025-04-25 09:00:00', '2025-04-25 09:00:00'),
(16, 'Action Camera', '4K action camera with waterproof case', 59.90, 'PROD-1016', '2025-05-05 10:10:00', '2025-05-05 10:10:00'),
(17, 'USB Cable', 'Durable braided USB-C cable, 1.5m', 3.49, 'PROD-1017', '2025-05-20 14:40:00', '2025-05-20 14:40:00'),
(18, 'Portable SSD', '1TB NVMe portable SSD', 89.95, 'PROD-1018', '2025-06-01 12:00:00', '2025-06-01 12:00:00'),
(19, 'Waterproof Jacket', 'Lightweight, breathable shell', 12.75, 'PROD-1019', '2025-06-15 08:20:00', '2025-06-15 08:20:00'),
(20, 'Home Projector', '1080p mini projector, HDMI input', 499.00, 'PROD-1020', '2025-07-01 20:00:00', '2025-07-01 20:00:00');

-- orders (20 rows) - totalPrice computed as price * quantity
INSERT INTO customer_order (order_id, customer_id, product_id, quantity, total_price, order_date) VALUES
(1, 3, 1, 2, 39.98, '2025-01-10 09:15:00'),
(2, 7, 6, 1, 249.99, '2025-01-22 14:40:00'),
(3, 1, 3, 5, 29.95, '2025-02-02 10:05:00'),
(4, 12, 10, 10, 29.90, '2025-02-18 16:20:00'),
(5, 5, 14, 1, 199.99, '2025-03-03 11:30:00'),
(6, 9, 20, 1, 499.00, '2025-03-15 19:10:00'),
(7, 15, 8, 3, 237.00, '2025-03-22 08:45:00'),
(8, 2, 2, 1, 49.50, '2025-04-01 12:00:00'),
(9, 18, 12, 2, 79.90, '2025-04-07 07:25:00'),
(10, 4, 5, 4, 39.80, '2025-04-12 17:55:00'),
(11, 11, 16, 1, 59.90, '2025-04-18 13:35:00'),
(12, 14, 7, 6, 86.94, '2025-04-20 15:10:00'),
(13, 6, 11, 3, 45.00, '2025-04-27 09:05:00'),
(14, 20, 9, 1, 299.00, '2025-05-02 18:00:00'),
(15, 8, 4, 1, 129.00, '2025-05-10 10:40:00'),
(16, 13, 13, 7, 52.50, '2025-05-16 14:00:00'),
(17, 16, 15, 2, 48.00, '2025-05-22 11:25:00'),
(18, 17, 18, 1, 89.95, '2025-05-28 20:15:00'),
(19, 19, 19, 5, 63.75, '2025-06-05 09:50:00'),
(20, 10, 17, 12, 41.88, '2025-06-12 07:30:00');

-- inventory (20 rows)
INSERT INTO inventory (inventory_id, product_id, quantity, location) VALUES
(1, 1, 120, 'Warehouse A - Bay 3'),
(2, 2, 45, 'Warehouse B - Bay 1'),
(3, 3, 300, 'Warehouse A - Bay 7'),
(4, 4, 12, 'Warehouse C - Shelf 2'),
(5, 5, 200, 'Warehouse B - Shelf 5'),
(6, 6, 8, 'Warehouse A - Bay 1'),
(7, 7, 150, 'Warehouse C - Shelf 3'),
(8, 8, 34, 'Warehouse B - Bay 4'),
(9, 9, 5, 'Warehouse A - Bay 2'),
(10, 10, 500, 'Warehouse C - Bin 12'),
(11, 11, 85, 'Warehouse B - Shelf 1'),
(12, 12, 40, 'Warehouse A - Bay 5'),
(13, 13, 220, 'Warehouse C - Bin 3'),
(14, 14, 16, 'Warehouse B - Bay 2'),
(15, 15, 60, 'Warehouse A - Shelf 4'),
(16, 16, 25, 'Warehouse C - Bay 6'),
(17, 17, 400, 'Warehouse B - Bin 7'),
(18, 18, 10, 'Warehouse A - Bay 8'),
(19, 19, 95, 'Warehouse C - Shelf 9'),
(20, 20, 3, 'Warehouse B - Bay 9');

