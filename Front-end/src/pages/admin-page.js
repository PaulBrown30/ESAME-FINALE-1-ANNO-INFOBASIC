import { AccountHeader } from "../components/accounts-header"
import { jd } from "../jd.config"
import { createSignal } from "@just-dom/signals"
import { effect } from "@just-dom/signals"
import { createRef } from "just-dom"
import { NoAccess } from "../components/no-access"

export function AdminPage() {

    const admin_id = location.pathname.replace("/admins/","")
    console.log(admin_id)

    const [Packages, SetPackages] = createSignal([])
    const [Couriers, SetCouriers] = createSignal([])
    const [AdminData, SetAdminData] = createSignal()
    const [Category, SetCategory] = createSignal("packages")
    const [Loading, SetLoading] = createSignal(false)

    const inputRef = createRef()

    const token = localStorage.getItem("token")
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
            
                fetch(`http://127.0.0.1:5000/api/packages`)
                .then(async (res) => {
                    const packages = await res.json()
                    console.log(packages)
                    if (res.ok) {
                        SetPackages(packages)
                    }
                })
                .catch((err) => {
                    console.log(err)
                })

            
                fetch(`http://127.0.0.1:5000/api/couriers`)
                .then(async (res) => {
                    const couriers = await res.json()
                    console.log(couriers)
                    if (res.ok) {
                        SetCouriers(couriers)
                    }
                })
                .catch((err) => {
                    console.log(err)
                })


        }
    })
    .catch((err) => {
        console.log(err)
    })
    .finally(() => {
        SetLoading(false)
    })


    return jd.div({},[
        jd.table({
            className: "flex flex-col h-screen bg-amber-200",
            ref: el => {
                effect(el,() => {
                    if (AdminData()){
                        el.replaceChildren(
                            AccountHeader(),
                            jd.tbody({
                                className: "container self-center mt-4 i overflow-x-auto",
                                ref: el => {
                                    effect(el, () => {
                                        if (!Loading()) {
                                            el.innerHTML = ""
                                            el.append(
                                                jd.div({className: "flex flex-row my-4 gap-4"},[
                                                    jd.div({ className: "flex flex-col px-6 py-3 bg-white rounded-xl "},[
                                                        jd.p({className: "font-bold"},["Admin:"]),
                                                        jd.p({
                                                            className:"",
                                                            ref: el => {
                                                                effect(el,() => {
                                                                    if (AdminData()) {
                                                                        el.textContent = `${AdminData().name} ${AdminData().surname}`                                                             
                                                                    }
                                                                })
                                                            }
                                                        })
                                                    ]),
                                                    jd.div({ 
                                                        className: "flex flex-row px-4 py-2 gap-4 bg-white rounded-xl items-center",
                                                        ref: el => {
                                                            effect(el, () => {
                                                                if (Category() == "packages") {
                                                                    el.replaceChildren(
                                                                        jd.button({className: "btn btn-disabled btn-lg bg-amber-200 text-white"},["Pagina Spedizioni"]),
                                                                        jd.button({
                                                                            className: "btn btn-lg bg-amber-400",
                                                                            onclick: () => {SetCategory("couriers")}
                                                                        },["Pagina Corrieri"])
                                                                    )
                                                                } else {
                                                                    el.replaceChildren(
                                                                        jd.button({
                                                                            className: "btn btn-lg bg-amber-400",
                                                                            onclick: () => {SetCategory("packages")}
                                                                        },["Pagina Spedizioni"]),
                                                                        jd.button({className: "btn btn-disabled btn-lg bg-amber-200 text-white"},["Pagina Corrieri"])
                                                                    )
                                                                }
                                                            })
                                                        }
                                                    },[]),
                                                    jd.div({className: "flex flex-row px-4 py-2 gap-4 bg-white rounded-xl items-center"},[
                                                        jd.a({
                                                            className: "btn btn-lg btn-primary",
                                                            href: ((Category() == "packages")? `/admins/${admin_id}/add_package` : `/admins/${admin_id}/add_courier`)
                                                        },[
                                                            jd.lucide("Plus",{className: "size-6"}),
                                                            jd.p({},["Aggiungi " + ((Category() == "packages")? "Spedizione" : "Corriere")])
                                                        ])
                                                    ])                                   
                                                ])
                                            );
                                            if (Category() == "packages" ) {
                                                el.append(...Packages().map(package_data => packageRow({package_data})))
                                            } else {
                                                el.append(...Couriers().map(courier_data => CourierRow({courier_data})))
                                            }
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
        jd.td({className: " p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Prezzo"]),
            jd.p({},[`${package_data.price} $  `])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Data di arrivo stimata"]),
            jd.p({},[`${package_data.estimated_arrival_date}`])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.div({className: "flex flex-row relative justify-between bg-white py-3 px-2 rounded-2xl shadow-lg gap-6"},[
                jd.div({className: "flex flex-col items-center " + (package_data.statuses.some(dizionario => dizionario.id === "S-001")? " text-amber-400" : "opacity-20")},[
                    jd.lucide("PackageCheck",{className: "size-10"}),
                    jd.p({className: "font-bold"},["Preso in Carico"])
                ]),
                jd.div({
                    ref: el => {
                        effect(el,() => {
                            if (!package_data.statuses.some(dizionario => dizionario.id === "S-103")) {
                                el.replaceChildren(
                                    jd.div({className: "flex flex-col items-center " + (package_data.statuses.some(dizionario => dizionario.id === "S-002")? " text-amber-400" : "opacity-20")},[
                                        jd.lucide("Van",{className: "size-10" }),
                                        jd.p({className: "font-bold"},["In consegna"])
                                    ])
                                )
                            } else {
                                el.replaceChildren(
                                    jd.div({className: "flex flex-col items-center text-red-700"},[
                                        jd.lucide("X",{className: "size-10"}),
                                        jd.p({className: "font-bold"},["Pacco non ritirato"])
                                    ])
                                )                                                        
                            }
                        })
                    }
                },[]),
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


function CourierRow({courier_data}) {
    return jd.tr({className: "mt-4 shadow-xl bg-amber-100 rounded-2xl border-2 m-2 mx-6 gap-3 "},[
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Nome Cognome"]),
            jd.p({},[`${courier_data.name} ${courier_data.surname}`])
        ]),
        jd.td({className: " p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Current Location"]),
            jd.p({},[`${courier_data.current_cap} CAP`])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Data di Nascita"]),
            jd.p({},[`${courier_data.birth_date}`])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Numero di Telefono"]),
            jd.p({},[`${courier_data.phone_number}`])
        ]),
        jd.td({className: "p-4 px-6 border-l-2 align-top"},[
            jd.p({className: "font-bold "},["Pacchi attivi"]),
            jd.p({},[`${courier_data.packages.length}/${courier_data.max_load}`])
        ]),
    ])
}



