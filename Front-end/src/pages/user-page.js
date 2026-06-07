import { AccountHeader } from "../components/accounts-header"
import { jd } from "../jd.config"
import { createSignal } from "@just-dom/signals"
import { effect } from "@just-dom/signals"

export function UserPage() {

    const user_id = location.pathname.replace("/users/","")
    console.log(user_id)

    const [UserPackages, SetUserPackages] = createSignal([])
    const [loading, SetLoading] = createSignal(false)

    fetch(`http://127.0.0.1:5000/api/users/${user_id}`)
    .then(async (res) => {
        SetLoading(true)
        const user_data = await res.json()
        console.log(user_data)
        const packages = user_data.packages
        console.log(packages)
        if (res.ok) {
            SetUserPackages(packages)
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
            className: "flex flex-col w-full h-screen bg-amber-200",
            ref: el => {
                effect(el,() => {
                    el.replaceChildren(
                        AccountHeader(),
                        jd.tbody({
                            className: "container self-center mt-4",
                            ref: el => {
                                effect(el, () => {
                                    if (!loading()) {
                                        el.innerHTML = ""
                                        el.append(...UserPackages().map(package_data => packageRow({package_data})))
                                    } else {
                                        jd.lucide("Loader2",{className: "animate-spin size-10"} )
                                    }
                                })
                            }
                        },[])
                    )
                })
            }
        },[])
    ])
}

function packageRow({package_data}) {
    return jd.tr({className: "mt-4 shadow-xl bg-amber-100 rounded-2xl border-2 m-2 mx-6 gap-3 "},[
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
            jd.div({className: "flex flex-row relative justify-between bg-white py-3 px-2 rounded-2xl shadow-lg gap-6"},[
                jd.div({className: "flex flex-col items-center " + (package_data.statuses.some(dizionario => dizionario.id === "S-001")? " text-amber-400" : "opacity-20")},[
                    jd.lucide("PackageCheck",{className: "size-10"}),
                    jd.p({className: "font-bold"},["Preso in Carico"])
                ]),
                jd.div({className: "flex flex-col items-center " + (package_data.statuses.some(dizionario => dizionario.id === "S-002")? " text-amber-400" : "opacity-20")},[
                    jd.lucide("Van",{className: "size-10" }),
                    jd.p({className: "font-bold"},["In consegna"])
                ]),
                jd.div({className: "flex flex-col items-center " + (package_data.statuses.some(dizionario => dizionario.id === "S-003")? " text-amber-400" : "opacity-20")},[
                    jd.lucide("Home",{className: "size-10"}),
                    jd.p({className: "font-bold"},["Consegnato"])
                ])
            ]),
        ])
    ])
}