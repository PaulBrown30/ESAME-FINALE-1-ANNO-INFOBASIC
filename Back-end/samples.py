from service import auth_service,admin_service,user_service,status_service,courier_service,package_service

def create_samples():
    admin_service.create({
        "name": "Paolo",
        "surname": "Marrone",
        "email": "admin@gmail.com",
        "password": "Admin1234."
    }) 

    courier_service.create({
        "name": "Paolo",
        "surname": "Marrone",
        "email": "courier@gmail.com",
        "password": "Courier1234.",
        "phone_number": "3774567865",
        "birth_date": "2001-11-30",
    })

    status_service.create({
        "id": "S-001",
        "name": "Preso in Carico",
        "description": "Il pacco è stato preso in carico!"
    })

    status_service.create({
        "id": "S-002",
        "name": "In Consegna",
        "description": "Il pacco è stato prelevato dal corriere!"
    })

    status_service.create({
        "id": "S-003",
        "name": "Consegnato",
        "description": "Il pacco è stato consegnato!"
    })

    status_service.create({
        "id": "S-101",
        "name": "Mancata Consegna",
        "description": "Il pacco non ha trovato il destinatario!"
    })

    status_service.create({
        "id": "S-102",
        "name": "Pacco Smarrito",
        "description": "Il pacco è stato smarrito!"
    })

    status_service.create({
        "id": "S-103",
        "name": "Pacco Non Ritirato",
        "description": "Il pacco non è stato ritirato!"
    })

    user_service.create({
        "name": "Paolo",
        "surname": "Marrone",
        "email": "adas@gmail.com",
        "password": "Sdwdd563."
    })

    user_service.create({
        "name": "test",
        "surname": "test",
        "email": "user@gmail.com",
        "password": "User1234."
    })

    package_service.create({
        "id": "1234567890",
        "weight": 76.55,
        "sender_name": "test assegnazione",
        "sender_surname": "Marrone",
        "sender_cap": "43121",   
        "receiver_name": "Gianni",
        "receiver_surname": "Celeste",
        "receiver_cap": "65124"
    })
    package_service.add_status("1234567890","S-002",2)
    package_service.add_status("1234567890","S-003",2)

    package_service.create({
        "id": "1234567891",
        "weight": 76.55,
        "sender_name": "Bruno",
        "sender_surname": "Marrone",
        "sender_cap": "10121",   
        "receiver_name": "Gianni",
        "receiver_surname": "Celeste",
        "receiver_cap": "65124"
    })

    package_service.add_status("1234567891","S-002",2)
    package_service.add_status("1234567891","S-102",2)


    package_service.create({
        "id": "1234567892",
        "weight": 76.55,
        "sender_name": "Brunoooooooooooooooooo",
        "sender_surname": "Marrone",
        "sender_cap": "20121",   
        "receiver_name": "Gianni",
        "receiver_surname": "Celeste",
        "receiver_cap": "35121"
    })

    package_service.create({
        "id": "1234567893",
        "weight": 76.55,
        "sender_name": "test non consegnato",
        "sender_surname": "Marrone",
        "sender_cap": "25121",  
        "receiver_name": "Gianni",
        "receiver_surname": "Celeste",
        "receiver_cap": "37121"
    })

    package_service.create({
        "id": "1234567894",
        "weight": 76.55,
        "sender_name": "test non consegnato",
        "sender_surname": "Marrone",
        "sender_cap": "25121",  
        "receiver_name": "Gianni",
        "receiver_surname": "Celeste",
        "receiver_cap": "37121"
    })


    user_service.add_package(4,"1234567890")
    user_service.add_package(4,"1234567891")