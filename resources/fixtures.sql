INSERT INTO users (username, password) VALUES
('user1','2acb428595cca4c51686ed0b344a410e70edb554825d11dd50c5396374820d323887effe68a37cc887aa18734a7588e6'),
('user2','886b02dfff5d48120ea4576be33c31a38847a2d222a0098cfadc6ff3a374ca1d52d5e7b7d4347f868b35ee1c5b5c0c47'),
('user3','9067116a522fee47d950640ea966ca773482d575d5de871ad2c785c8bbcec6fd104ba7977eb8960d680837b061872870');

INSERT INTO todos (user_id, description, completed) VALUES
(1, 'Vivamus tempus', 0),
(1, 'lorem ac odio', 0),
(1, 'Ut congue odio', 0),
(1, 'Sodales finibus', 1),
(1, 'Accumsan nunc vitae', 0),
(2, 'Lorem ipsum', 1),
(2, 'In lacinia est', 0),
(2, 'Odio varius gravida', 0);
