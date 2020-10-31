const db = connect("mongodb://root:personalguide2020@localhost:27017/database");

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