db.createUser(
    {
        user: System.getenv("MONGO_USER"),
        pwd: System.getenv("MONGO_PASSWORD"),
        roles: [
            {
                role: "readWrite",
                db: System.getenv("MONGO_DATABASE")
            }
        ]
    }
)