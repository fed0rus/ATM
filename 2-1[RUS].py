INSERT INTO result (res) VALUES((SELECT SUM(val) FROM transactions WHERE recipient='Frank') - (SELECT SUM(val) FROM transactions WHERE sender='Frank'));
