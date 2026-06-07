import { jd } from "../jd.config"

export function NotFoundPage() {
    return jd.div({className: "flex flex-col bg-amber-400 h-screen w-screen items-center justify-center"},[
        jd.img({className: "h-50" ,src:"/assets/LumacaExpress_logo.png"},[]),
        jd.div({className: "card"},[
            jd.div({className: "card-body bg-amber-300"},[
                jd.p({className:"text-5xl font-bold text-amber-700"},["PAGINA NON TROVATA"]),
                jd.a({
                    className: "btn btn-lg bg-gray-900 text-white mt-4",
                    href: "/home"
                },["Torna alla home"])
            ])
        ])           
    ])
}