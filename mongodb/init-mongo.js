var db = connect("mongodb://localhost/admin");

db = db.getSiblingDB('database'); // we can not use "use" statement here to switch db


db.createUser(
    {
        user: "user",
        pwd: "personalguide2020",
        roles: [
            {
                role: "readWrite",
                db: "database"
            }
        ],
    }
)