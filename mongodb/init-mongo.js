db.createUser(
    {
        user: "user",
        pwd: "personalguide2020",
        roles: [
            {
                role: "readWrite",
                db: "database"
            }
        ]
    }
)