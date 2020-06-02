db.createUser(
        {
            user: "user",
            pwd: "password",
            roles: [
                {
                    role: "readWrite",
                    db: "flask_db"
                }
            ]
        }
);
