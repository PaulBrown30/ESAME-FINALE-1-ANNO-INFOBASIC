import { jd } from "../jd.config";
import { createSignal } from "@just-dom/signals";
import { createRef } from "just-dom";
import { effect } from "@just-dom/signals";

 
export function AddCourierPage() {

    const token = localStorage.getItem("token")
    const admin_id = location.pathname.replace("/admins/","").replace("/add_courier","")
    console.log(admin_id)    
    
    const passwordInputRef = createRef();
    const [PasswordVisible, SetPasswordVisible] = createSignal(false);
    const [Loading,SetLoading] = createSignal(false);
    const [EmailError, SetEmailError] = createSignal(false);
    const [AdminData, SetAdminData] = createSignal()

    SetLoading(true)

    fetch(`http://127.0.0.1:5000/api/admins/${admin_id}`,
        {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        }
    )
    .then(async (res) => {
        const admin_data = await res.json()
        console.log(admin_data)
        if (res.ok) {
            SetAdminData(admin_data)
        } 
    })
    .catch((err) => {
        console.log(err)
    })
    .finally(() => {
        SetLoading(false)
    })
    
    
    

    const HandleSubmit = async (e) => {
        SetLoading(true)
        SetEmailError(false)
        e.preventDefault()

        const dataform = new FormData(e.target)
        const data = Object.fromEntries(dataform)
        console.log(data)
        fetch(`http://127.0.0.1:5000/api/couriers/create`,
            {method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        })
        .then(async (res)=> {
            const data = await res.json()
            console.log(data)
            if(!res.ok) {
                SetEmailError(true)            
            } else {
                document.location.pathname = `/admins/${admin_id}`
            }
        })
        .catch((err)=> {
            console.log(err)
            SetEmailError(true)
        })
        .finally(() => {
            SetLoading(false)
        })
    }

    return jd.div({
        className: "flex flex-col bg-amber-400 h-screen w-screen items-center justify-center",
        ref: el => {
            effect(el, () => {
                if (AdminData()) { 
                    el.replaceChildren(
                        jd.img({className: "h-50" ,src:"/assets/LumacaExpress_logo.png"},[]),
                        jd.form({
                            className: "card w-100 shadow-2xl bg-amber-100",
                            onsubmit: HandleSubmit
                        },[
                            jd.div({className: "card-body flex flex-col gap-3"},[
                                jd.p({className: "text-2xl"},["Aggiunta Corriere"]),
                                jd.div({},[
                                    jd.label({className: "input validator w-full"},[
                                        jd.lucide("User2",{className:"size-5"}),
                                        jd.input({
                                            placeholder: "Inserisci nome",
                                            id: "name",
                                            name: "name",
                                            type: "text",
                                            minLength: 3,
                                            maxLength: 30,
                                            required: "true"
                                        },[])
                                    ]),
                                    jd.p({className:"validator-hint hidden"},[
                                        "Il Nome deve avere almeno 3 caratteri!"
                                    ]),
                                ]),
                                jd.div({},[
                                    jd.label({className: "input validator w-full"},[
                                        jd.lucide("User2",{className:"size-5"}),
                                        jd.input({
                                            placeholder: "Inserisci cognome",
                                            id: "surname",
                                            name: "surname",
                                            type: "text",
                                            minLength: 3,
                                            maxLength: 30,
                                            required: "true"
                                        },[])
                                    ]),
                                    jd.p({className:"validator-hint hidden"},[
                                        "Il Cognome deve avere almeno 3 caratteri!"
                                    ]),
                                ]),
                                jd.div({},[
                                    jd.label({className: "input validator w-full"},[
                                        jd.lucide("Phone",{className:"size-5"}),
                                        jd.input({
                                            placeholder: "Inserisci Numero di telefono",
                                            id: "phone_number",
                                            name: "phone_number",
                                            type: "text",
                                            minLength: 10,
                                            maxLength: 10,
                                            inputmode: "numeric",
                                            required: "true"
                                        },[])
                                    ]),
                                    jd.p({className:"validator-hint hidden"},[
                                        "Il numero di telefono deve avere 10 caratteri numerici!"
                                    ]),
                                ]),
                                jd.div({},[
                                    jd.label({className: "input validator w-full"},[
                                        jd.lucide("Calendar",{className:"size-5"}),
                                        jd.input({
                                            placeholder: "Inserisci Data di nascita",
                                            id: "birth_date",
                                            name: "birth_date",
                                            type: "date",
                                            required: "true"
                                        },[])
                                    ]),
                                    jd.p({className:"validator-hint hidden"},[
                                        "La data di Nascita deve essere valida!"
                                    ]),
                                ]),
                                jd.div({},[
                                    jd.label({className: "input validator w-full"},[
                                        jd.lucide("Mail",{className:"size-5"}),
                                        jd.input({
                                            placeholder: "Inserisci email",
                                            id: "email",
                                            name: "email",
                                            type: "email",
                                            minLength: 3,
                                            maxLength: 30,
                                            pattern: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+[.][a-zA-Z]{2,}",
                                            required: "true"
                                        },[])
                                    ]),
                                    jd.p({className:"validator-hint hidden"},[
                                        "Inserisci un email valida"
                                    ]),
                                    jd.div({
                                        className:"flex",
                                        ref: el => {
                                            effect(el,() => {
                                                if (EmailError()) {
                                                    el.replaceChildren(
                                                        jd.p({ className: "px-2 pt-2 text-red-400"},["Email gia utilizzata!"])
                                                    )
                                                } else {
                                                    el.replaceChildren()                                    
                                                }
                                            })
                                        }
                                    },[])
                                ]),
                                jd.div({},[
                                    jd.label({className: "input validator w-full"},[
                                        jd.lucide("LockKeyhole",{className:"size-5"}),
                                        jd.input({
                                            ref: passwordInputRef,
                                            placeholder: "Inserisci password",
                                            id: "password",
                                            name: "password",
                                            type: "password",
                                            minLength: 3,
                                            maxLength: 30,
                                            pattern: "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])[^ ]{8,}",
                                            required: "true"
                                        },[]),
                                        jd.button({
                                            className: `btn btn-xs`,
                                            type: "button",
                                            onclick: () => {
                                                passwordInputRef.current.type = passwordInputRef.current.type == "password"? "text": "password";
                                                SetPasswordVisible(PasswordVisible() == false ? true : false)
                                            }
                                        },[
                                            jd.div({
                                                ref: el => {
                                                    effect(el, () => {
                                                        if (PasswordVisible()) {
                                                            el.replaceChildren(jd.lucide("Eye",{className:"size-5" },[]))
                                                        } else {
                                                            el.replaceChildren(jd.lucide("EyeClosed",{className:"size-5" },[]))
                                                        }
                                                    })
                                                }
                                            },[])
                                        ]),
                                    ]),
                                    jd.p({className:"validator-hint hidden"},[
                                        "Inserisci una password valida"
                                    ]),
                                ]),
                            ]),
                            jd.button({ 
                                className: "m-2 btn bg-gray-800 text-white",
                                type: "submit",
                                ref: el => {
                                    effect(el, () => {
                                        if (Loading()) {
                                            el.classList.add("btn-disabled");
                                            el.classList.add("opacity-50")
                                        } else {
                                            el.classList.remove("btn-disabled")
                                            el.classList.remove("opacity-50")
                                        }
                                    })
                                }
                            },["Registra"])
                        ])
                    )
                } else {
                    el.replaceChildren(
                        jd.img({className: "h-50" ,src:"/assets/LumacaExpress_logo.png"},[]),
                        jd.lucide("Loader",{className: "size-10 animate-spin"})
                    )
                }
            })
        }    
    },[
    ])
}
