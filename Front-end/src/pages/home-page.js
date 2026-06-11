import { createRef } from "just-dom";
import { HomeHeader } from "../components/home-header";
import { jd } from "../jd.config";
import { createSignal } from "@just-dom/signals";
import { effect } from "@just-dom/signals";

export function HomePage() {

    const inputRef = createRef();
    const [PackageData, SetPackageData] = createSignal();
    const [Loading,SetLoading] = createSignal(false)
    const [Searched, SetSearched] = createSignal(false)

    function HandleTracking (package_code) {
        console.log(package_code)
        SetLoading(true)
        fetch(`http://127.0.0.1:5000/api/packages/${package_code}`)
        .then(async res => {
            const package_data = await res.json()
            console.log(package_data)
            if (res.ok){
                SetPackageData(package_data)
            } else {
                SetPackageData()
            }
        })
        .catch(err => {
            console.log(err)
        })
        .finally(() => {
            SetLoading(false)
            SetSearched(true)
        })
    }

    return jd.div({className:"flex flex-col"},[
        HomeHeader(),
        jd.div({className: "flex relative justify-center"},[
            jd.img({className: "h-200 w-full object-cover object-top",src:"./assets/homepage.png"},[]),
            jd.div({className:"flex flex-col absolute z-10 top-48 gap-4"},[
                jd.div({ className: "flex px-6 py-3 bg-gray-900 rounded-xl"},[
                    jd.p({className: "text-2xl text-white font-bold"},["TRACCIA IL TUO PACCO"])
                ]),
                jd.label({className: "flex flex-row bg-white items-center h-20 input align-bottom outline-0 w-150"},[
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
                    },["Traccia"])
                ]),
                jd.div({
                    ref: el => {
                        effect(el, () => {
                            if (PackageData()) {
                                el.replaceChildren(jd.div({className: "flex flex-col w-full bg-amber-400 p-2 px-6 rounded-2xl"},[
                                    jd.div({className: "flex flex-row relative justify-between my-5 bg-white py-3 px-2 rounded-2xl shadow-lg"},[
                                        jd.div({className: "flex flex-col items-center " + (PackageData().statuses.some(dizionario => dizionario.id === "S-001")? " text-amber-400" : "opacity-20")},[
                                           jd.lucide("PackageCheck",{className: "size-10"}),
                                           jd.p({className: "font-bold"},["Preso in Carico"])
                                        ]),
                                        jd.div({
                                            ref: el => {
                                                effect(el,() => {
                                                    if (!PackageData().statuses.some(dizionario => dizionario.id === "S-103")) {
                                                        el.replaceChildren(
                                                            jd.div({className: "flex flex-col items-center " + (PackageData().statuses.some(dizionario => dizionario.id === "S-002")? " text-amber-400" : "opacity-20")},[
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
                                                    if (!PackageData().statuses.some(dizionario => dizionario.id === "S-101" || dizionario.id === "S-102")) {
                                                        el.replaceChildren(
                                                            jd.div({className: "flex flex-col items-center " + (PackageData().statuses.some(dizionario => dizionario.id === "S-003")? " text-amber-400" : "opacity-20")},[
                                                                jd.lucide("Home",{className: "size-10"}),
                                                                jd.p({className: "font-bold"},["Consegnato"])
                                                            ])
                                                        )
                                                    } else {
                                                        el.replaceChildren(
                                                            jd.div({className: "flex flex-col items-center text-red-700"},[
                                                                jd.lucide("X",{className: "size-10"}),
                                                                jd.p({className: "font-bold"},[PackageData().statuses.some(dizionario => dizionario.id === "S-101")? "Non Consegnato": "Pacco smarrito"])
                                                            ])
                                                        )                                                        
                                                    }
                                                })
                                            }
                                        },[])

                                    ]),
                                    jd.div({className: "flex flex-row w-full justify-between rounded-2xl bg-white shadow-lg py-3 px-4 mb-5"},[
                                        jd.div({className: "flex flex-col h-full"},[
                                            jd.div({className: "flex flex-col"},[
                                                jd.p({className: "font-bold "},["Mittente"]),
                                                jd.p({},[`${PackageData().sender_name} ${PackageData().sender_surname}  CAP.${PackageData().sender_cap}`])
                                            ]),
                                            jd.div({className: "flex flex-col"},[
                                                jd.p({className: "font-bold "},["Destinatario"]),
                                                jd.p({},[`${PackageData().receiver_name} ${PackageData().receiver_surname}  CAP.${PackageData().receiver_cap}`])
                                            ]),
                                            jd.div({className: "flex flex-col"},[
                                                jd.p({className: "font-bold "},["Codice Corriere"]),
                                                jd.p({},[`${PackageData().courier_id}`])
                                            ])
                                        ]),
                                        jd.div({className: "flex flex-col h-full text-right"},[
                                            jd.div({className: "flex flex-col"},[
                                                jd.p({className: "font-bold "},[PackageData().actual_arrival_date? "Data di arrivo" : "Data stimata di arrivo"]),
                                                jd.p({},[PackageData().actual_arrival_date? `${PackageData().actual_arrival_date}`: `${PackageData().estimated_arrival_date}`])
                                            ]),
                                            jd.div({className: "flex flex-col"},[
                                                jd.p({className: "font-bold "},["Peso"]),
                                                jd.p({},[`${PackageData().weight} Kg`])
                                            ])
                                        ])
                                    ])
                                ]))
                            } else if (!Searched()) {
                                el.replaceChildren(jd.div({},[]))
                            } else {
                                el.replaceChildren(jd.div({className: "flex h-20 w-full bg-white rounded-2xl"},[
                                    jd.p({className: "self-center text-3xl m-auto font-bold text-red-500"},["Nessun Pacco Trovato!"])
                                ]))
                            }
                        })
                    }
                },[])
            ])          
        ])
    ])
} 