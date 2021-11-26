# login mysql
```sh
mysql -u root -p
```

# show password policy:
```sql
SHOW VARIABLES LIKE 'validate_password%';
```

# example: how to change policy:
```sql
SET GLOBAL validate_password.special_char_count = 0;
```

# change password
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass';
```