from werkzeug.security import generate_password_hash

print(generate_password_hash('admin123'))
print(generate_password_hash('user1pass'))
print(generate_password_hash('user2pass'))
