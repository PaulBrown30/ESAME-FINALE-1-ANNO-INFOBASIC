import { jd } from "../jd.config";
import { createSignal } from "@just-dom/signals";
import { createRef } from "just-dom";
import { effect } from "@just-dom/signals";

 
export function AddPackagePage() {
    const token = localStorage.getItem("token")
    const admin_id = location.pathname.replace("/admins/","").replace("/add_package","")
    console.log(admin_id)    
    
    const passwordInputRef = createRef();
    const [Loading,SetLoading] = createSignal(false);
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
        e.preventDefault()

        const dataform = new FormData(e.target)
        const data = Object.fromEntries(dataform)
        console.log(data)
        fetch(`http://127.0.0.1:5000/api/packages/create`,
            {method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        })
        .then(async (res)=> {
            const data = await res.json()
            console.log(data)
            if(!res.ok) {      
            } else {
                document.location.pathname = `/admins/${admin_id}`
            }
        })
        .catch((err)=> {
            console.log(err)
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
                            className: "card w-200 shadow-2xl bg-amber-100",
                            onsubmit: HandleSubmit
                        },[
                            jd.div({className: "card-body flex flex-col gap-3"},[
                                jd.p({className: "text-2xl border-b pb-2"},["Aggiunta Spedizione"]),
                                jd.p({},["Dati Mittente"]),
                                jd.div({className: "flex flex-row gap-3 align-bottom"},[
                                    jd.div({className: "w-full"},[
                                        jd.label({className: "input validator w-full"},[
                                            jd.lucide("User2",{className:"size-5"}),
                                            jd.input({
                                                placeholder: "Inserisci nome",
                                                id: "sender_name",
                                                name: "sender_name",
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
                                    jd.div({className: "w-full"},[
                                        jd.label({className: "input validator w-full"},[
                                            jd.lucide("User2",{className:"size-5"}),
                                            jd.input({
                                                placeholder: "Inserisci cognome",
                                                id: "sender_surname",
                                                name: "sender_surname",
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
                                    jd.div({className: "w-full"},[
                                        jd.label({className: "input validator w-full"},[
                                            jd.lucide("MapPin",{className:"size-5"}),
                                            jd.input({
                                                placeholder: "Inserisci il CAP",
                                                id: "sender_cap",
                                                name: "sender_cap",
                                                type: "text",
                                                minLength: 5,
                                                maxLength: 5,
                                                inputmode: "numeric",
                                                required: "true"
                                            },[])
                                        ]),
                                        jd.p({className:"validator-hint hidden"},[
                                            "Il CAP deve avere 5 caratteri numerici!"
                                        ]),
                                    ]),
                                ]),
                                jd.p({},["Dati Destinatario"]),
                                jd.div({className: "flex flex-row gap-3 align-bottom"},[
                                    jd.div({className: "w-full"},[
                                        jd.label({className: "input validator w-full"},[
                                            jd.lucide("User2",{className:"size-5"}),
                                            jd.input({
                                                placeholder: "Inserisci nome",
                                                id: "receiver_name",
                                                name: "receiver_name",
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
                                    jd.div({className: "w-full"},[
                                        jd.label({className: "input validator w-full"},[
                                            jd.lucide("User2",{className:"size-5"}),
                                            jd.input({
                                                placeholder: "Inserisci cognome",
                                                id: "receiver_surname",
                                                name: "receiver_surname",
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
                                    jd.div({className: "w-full"},[
                                        jd.label({className: "input validator w-full"},[
                                            jd.lucide("MapPin",{className:"size-5"}),
                                            jd.input({
                                                placeholder: "Inserisci il CAP",
                                                id: "receiver_cap",
                                                name: "receiver_cap",
                                                type: "text",
                                                minLength: 5,
                                                maxLength: 5,
                                                inputmode: "numeric",
                                                required: "true"
                                            },[])
                                        ]),
                                        jd.p({className:"validator-hint hidden"},[
                                            "Il CAP deve avere 5 caratteri numerici!"
                                        ]),
                                    ]),
                                ]),
                                jd.div({},["Dati Pacco"]),
                                jd.div({className: "w-full"},[
                                    jd.label({className: "input validator w-full"},[
                                        jd.lucide("Weight",{className:"size-5"}),
                                        jd.input({
                                            placeholder: "Inserisci il peso in Kg.",
                                            id: "weight",
                                            name: "weight",
                                            type: "number",
                                            min: 0.01,
                                            step:0.01,
                                            max: 999.99,
                                            maxLength: 6,
                                            required: "true",
                                        },[])
                                    ]),
                                    jd.p({className:"validator-hint hidden"},[
                                        "Il Peso deve essere tra 0.01 e 999.99!"
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