import { jd } from "../jd.config";

export function HomeHeader() {
    

    return jd.div({className: "flex flex-col"},[
        jd.div({className: "h-20 w-full bg-amber-400"},[
            jd.div({className: " h-full container flex flex-row items-center justify-between m-auto"},[
                jd.img({className: "h-30" ,src:"./assets/LumacaExpress_logo.png"}),
                jd.div({ className: "flex flex-row gap-2"},[
                    jd.button({className: "btn btn-lg bg-amber-300 btn-ghost", href: "/users/register"}, ["Sign up"]),
                    jd.button({className: "btn btn-lg bg-amber-300 btn-ghost"}, ["Log in"])   
                ]) 
            ])
        ]),
        jd.div({className: "flex flex-row h-16 border-b bg-white border-gray-400"},[
            jd.div({className: "pl-10 h-full container flex flex-row gap-6 items-center m-auto"},[
                jd.a({className: location.pathname == "/home"? "font-bold text-md hover:underline border-l-2 p-2 " : " text-md hover:underline p-2 border-l" , href: "/home"},["Home"]),
                jd.a({className: location.pathname == "/contattaci"? "font-bold text-md hover:underline border-l-2 p-2" : " text-md hover:underline p-2 border-l" , href: "/contattaci"},["Contattaci"])
            ])        
        ])         
    ])
}