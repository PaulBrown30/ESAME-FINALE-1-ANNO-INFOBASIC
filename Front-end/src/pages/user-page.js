import { AccountHeader } from "../components/accounts-header"
import { jd } from "../jd.config"
import { createSignal } from "@just-dom/signals"
import { effect } from "@just-dom/signals"
import { createRef } from "just-dom"
import { NoAccess } from "../components/no-access"

export function UserPage() {

    const user_id = location.pathname.replace("/users/","")
    console.log(user_id)

    const [UserPackages, SetUserPackages] = createSignal([])
    const [UserData, SetUserData] = createSignal()
    const [Loading, SetLoading] = createSignal(false)
    const [Searched, SetSearched] = createSignal(false)
    const inputRef = createRef()

    const token = localStorage.getItem("token")
    SetLoading(true)

    fetch(`http://127.0.0.1:5000/api/users/${user_id}`,
        {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        }
    )
    .then(async (res) => {
        const user_data = await res.json()
        console.log(user_data)
        const packages = user_data.packages
        console.log(packages)
        if (res.ok) {
            SetUserData(user_data)
            SetUserPackages(packages)
        }
    })
    .catch((err) => {
        console.log(err)
    })
    .finally(() => {
        SetLoading(false)
    })

    function HandleTracking (package_code) {
        console.log(package_code)
        SetLoading(true)
        fetch(`http://127.0.0.1:5000/api/users/${user_id}/add_package`,
            {method: "POST",
            body: JSON.stringify({"package_id":package_code}),
            headers: {"Content-Type": "application/json"}}
        )
        .then(async res => {
            const package_data = await res.json()
            console.log(package_data)
            if (res.ok){
                SetSearched("ok")
                SetUserPackages([...UserPackages(),package_data])
            } else {
                SetSearched("not-ok")
                SetUserPackages(UserPackages())
            }
        })
        .catch(err => {
            console.log(err)
        })
        .finally(() => {
            SetLoading(false)
        })
    }

    return jd.div({},[
        jd.table({
            className: "flex flex-col w-full h-screen bg-amber-200",
            ref: el => {
                effect(el,() => {
                    if (UserData()){
                        el.replaceChildren(
                            AccountHeader(),
                            jd.tbody({
                                className: "container self-center mt-4 overflow-x-auto",
                                ref: el => {
                                    effect(el, () => {
                                        if (!Loading()) {
                                            el.innerHTML = ""
                                            el.append(
                                                jd.div({className: "flex flex-row my-4 gap-4"},[
                                                    jd.div({ className: "flex flex-col px-6 py-3 bg-white rounded-xl "},[
                                                        jd.p({className: "font-bold"},["Utente:"]),
                                                        jd.p({
                                                            className:"",
                                                            ref: el => {
                                                                effect(el,() => {
                                                                    if (UserData()) {
                                                                        el.textContent = `${UserData().name} ${UserData().surname}`                                                             
                                                                    }
                                                                })
                                                            }
                                                        })
                                                    ]),
                                                    jd.label({className: "flex flex-row bg-white items-center h-20 input align-bottom outline-0 w-100"},[
                                                        jd.div({
                                                            ref: (el) => {
                                                                effect((el),() => {
                                                                    if (!Loading()) {
                                                                        el.replaceChildren(jd.lucide("Package",{className: "size-8"}))
                                                                    } else {
                                                                        el.replaceChildren(jd.lucide("Package",{className: "size-8 animate-spin"}))
                                                                    }
                                                                })
                                                            }
                                                        },[                        
                                                        ]),
                                                        jd.input({
                                                            className: " h-10 p-2",
                                                            placeholder:"Inserisci il codice...",
                                                            maxLength: 10,
                                                            ref: inputRef
                                                        },[]),
                                                        jd.button({
                                                            className: "btn btn-lg bg-amber-400 text-white",
                                                            onclick:() => {HandleTracking(inputRef.current.value)}
                                                        },["Aggiungi"])
                                                    ]),
                                                    jd.div({
                                                        className:"",
                                                        ref: el => {
                                                            effect(el,() => {
                                                                if (!Searched()) {
                                                                    el.replaceChildren()
                                                                } else {
                                                                    el.replaceChildren(
                                                                        jd.div({className: "flex flex-row bg-white items-center h-20 w-100 rounded-lg p-4 shadow-md"},[
                                                                            jd.p({className: Searched() == "ok"? "text-2xl text-green-500 font-bold": "text-2xl text-red-500 font-bold" },[
                                                                                Searched() == "ok"? "Pacco aggiunto": "Pacco non aggiunto"
                                                                            ])
                                                                        ])
                                                                    )
                                                                }
                                                            })
                                                        }
                                                    },[])                                         
                                                ])
                                            );
                                            el.append(...UserPackages().map(package_data => packageRow({package_data})))
                                        } else {
                                            jd.lucide("Loader2",{className: "animate-spin size-10"} )
                                        }
                                    })
                                }
                            },[])
                        )
                    } else if (Loading()) {
                    el.replaceChildren(
                        jd.div({className: "flex h-screen w-screen justify-center items-center"},[
                            jd.lucide("Loader",{className: "animate-spin size-10"})
                        ])
                    )
                    } else {
                        el.replaceChildren(NoAccess())
                    }
                })
            }
        },[])
    ])
}

function packageRow({package_data}) {
    return jd.tr({className: "mt-4 shadow-xl bg-amber-100 rounded-2xl border-2 m-2 mx-6 gap-3 "},[
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Codice"]),
            jd.p({},[`${package_data.id}`])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Mittente"]),
            jd.p({},[`${package_data.sender_name} ${package_data.sender_surname}`]),
            jd.p({},[`CAP. ${package_data.sender_cap}`]),
        ]),
        jd.td({className: " p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Destinatario"]),
            jd.p({},[`${package_data.receiver_name} ${package_data.receiver_surname}`]),
            jd.p({},[`CAP. ${package_data.receiver_cap}`]),
        ]),
        jd.td({className: " p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Peso"]),
            jd.p({},[`${package_data.weight} kg.`])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Data di arrivo stimata"]),
            jd.p({},[`${package_data.estimated_arrival_date}`])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Data di arrivo effettiva"]),
            jd.p({},[package_data.actual_arrival_date? `${package_data.actual_arrival_date}` : "Non Disponibile"])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.div({className: "flex flex-row relative justify-between bg-white py-3 px-2 rounded-2xl shadow-lg gap-6"},[
                jd.div({className: "flex flex-col items-center " + (package_data.statuses.some(dizionario => dizionario.id === "S-001")? " text-amber-400" : "opacity-20")},[
                    jd.lucide("PackageCheck",{className: "size-10"}),
                    jd.p({className: "font-bold"},["Preso in Carico"])
                ]),
                jd.div({className: "flex flex-col items-center " + (package_data.statuses.some(dizionario => dizionario.id === "S-002")? " text-amber-400" : "opacity-20")},[
                    jd.lucide("Van",{className: "size-10" }),
                    jd.p({className: "font-bold"},["In consegna"])
                ]),
                jd.div({
                    ref: el => {
                        effect(el,() => {
                            if (!package_data.statuses.some(dizionario => dizionario.id === "S-101" || dizionario.id === "S-102")) {
                                el.replaceChildren(
                                    jd.div({className: "flex flex-col items-center " + (package_data.statuses.some(dizionario => dizionario.id === "S-003")? " text-amber-400" : "opacity-20")},[
                                        jd.lucide("Home",{className: "size-10"}),
                                        jd.p({className: "font-bold"},["Consegnato"])
                                    ])
                                )
                            } else {
                                el.replaceChildren(
                                    jd.div({className: "flex flex-col items-center text-red-700"},[
                                        jd.lucide("X",{className: "size-10"}),
                                        jd.p({className: "font-bold"},[package_data.statuses.some(dizionario => dizionario.id === "S-101")? "Non Consegnato": "Pacco smarrito"])
                                    ])
                                )                                                        
                            }
                        })
                    }
                },[])
            ]),
        ])
    ])
}