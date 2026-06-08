import { jd } from "../jd.config";

export function NoAccess() {

    return  jd.div({className: "flex h-screen w-screen justify-center bg-amber-400 "},[
                jd.div({className:"flex flex-col items-center self-center bg-amber-300 p-4 rounded-lg"},[
                    jd.p({className: "text-3xl font-bold"},["Non hai Accesso a questa Pagina!"]),
                    jd.div({className: "flex flex-row gap-4 my-4"},[
                        jd.a({className: "btn btn-lg bg-gray-900 text-white border-0", href: "/login"},["Vai al Login"]),
                        jd.a({className: "btn btn-lg bg-gray-900 text-white border-0", href: "/home"},["Vai alla Home"])                               
                    ])
                ])
    ])
                
}