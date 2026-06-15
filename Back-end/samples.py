from service import admin_service,user_service,status_service,courier_service,package_service

def create_samples():
    admin_service.create({
        "name": "Test",
        "surname": "Admin",
        "email": "admin@gmail.com",
        "password": "Admin1234."
    }) 

    courier_service.create({
        "name": "Test",
        "surname": "Corriere",
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


    status_service.add_ammitted_transition("S-001","S-002")
    status_service.add_ammitted_transition("S-001","S-103")
    status_service.add_ammitted_transition("S-002","S-003")
    status_service.add_ammitted_transition("S-002","S-101")
    status_service.add_ammitted_transition("S-002","S-102")

    user_service.create({
        "name": "Paolo",
        "surname": "Marrone",
        "email": "adas@gmail.com",
        "password": "Sdwdd563."
    })

    user_service.create({
        "name": "Test",
        "surname": "User",
        "email": "user@gmail.com",
        "password": "User1234."
    })

    package_service.create({
        "id": "1234567890",
        "weight": 76.55,
        "sender_name": "Gianni",
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
        "sender_surname": "Bucci",
        "sender_cap": "10121",   
        "receiver_name": "Andrea",
        "receiver_surname": "Di Simone",
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

    courier_service.create({
        "name": "Filippo",
        "surname": "Verdi",
        "email": "filippo.verdi@gmail.com",
        "password": "Courier9999.",
        "phone_number": "3339876543",
        "birth_date": "1992-04-15",
    })

    package_service.create({
        "id": "1234567900",
        "weight": 2.50,
        "sender_name": "Mario",
        "sender_surname": "Rossi",
        "sender_cap": "00186",  
        "receiver_name": "Luca",
        "receiver_surname": "Bianchi",
        "receiver_cap": "20121"
    })
    package_service.add_status("1234567900", "S-002", 5)

    package_service.create({
        "id": "1234567901",
        "weight": 10.40,
        "sender_name": "Laura",
        "sender_surname": "Neri",
        "sender_cap": "50123",  
        "receiver_name": "Elena",
        "receiver_surname": "Gialli",
        "receiver_cap": "80138"
    })
    package_service.add_status("1234567901", "S-002", 5)
    package_service.add_status("1234567901", "S-003", 5)

    package_service.create({
        "id": "1234567902",
        "weight": 0.85,
        "sender_name": "Stefano",
        "sender_surname": "Viola",
        "sender_cap": "10122", 
        "receiver_name": "Anna",
        "receiver_surname": "Verdi",
        "receiver_cap": "40121"
    })
    package_service.add_status("1234567902", "S-002", 5)
    package_service.add_status("1234567902", "S-101", 5)

    package_service.create({
        "id": "1234567903",
        "weight": 15.00,
        "sender_name": "Azienda XYZ",
        "sender_surname": "Spedizioni",
        "sender_cap": "16121", 
        "receiver_name": "Giorgio",
        "receiver_surname": "Rosa",
        "receiver_cap": "90133"
    })
    package_service.add_status("1234567903", "S-002", 5)
    package_service.add_status("1234567903", "S-102", 5)