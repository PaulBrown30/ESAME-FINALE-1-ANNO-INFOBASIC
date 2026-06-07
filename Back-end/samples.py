from service import auth_service,admin_service,user_service,status_service,courier_service,package_service

def create_samples():
    admin_service.create({
        "name": "Paolo",
        "surname": "Marrone",
        "email": "paolo.marrone1@gmail.com",
        "password": "Password30."
    }) 

    courier_service.create({
        "name": "Paolo",
        "surname": "Marrone",
        "email": "paolo.marronewdwa5@gmail.com",
        "password": "Password30.",
        "phone_number": "3774567865",
        "max_load" : 10,
        "birth_date": "01/01/42"
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

    user_service.create({
        "name": "Paolo",
        "surname": "Marrone",
        "email": "paolo.marrone2@gmail.com",
        "password": "Password30."
    })

    user_service.create({
        "name": "test",
        "surname": "test",
        "email": "test@gmail.com",
        "password": "Testsuper30."
    })

    package_service.create({
        "id": "1234567890",
        "price": 76.55,
        "weight": 76.55,
        "sender_name": "Bruno",
        "sender_surname": "Marrone",
        "sender_cap": "65124",
        "receiver_name": "Gianni",
        "receiver_surname": "Celeste",
        "receiver_cap": "65124",
        "estimated_arrival_date": "11/11/2026",
        "courier_id":2
    })

    package_service.create({
        "id": "1234567891",
        "price": 76.55,
        "weight": 76.55,
        "sender_name": "Brunoooooooooooooooooo",
        "sender_surname": "Marrone",
        "sender_cap": "65124",
        "receiver_name": "Gianni",
        "receiver_surname": "Celeste",
        "receiver_cap": "65124",
        "estimated_arrival_date": "11/11/2026",
        "courier_id":2
    })

    package_service.add_status("1234567891","S-002")
    package_service.add_status("1234567891","S-003")

    user_service.add_package(4,"1234567890")
    user_service.add_package(4,"1234567891")