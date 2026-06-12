import { jd } from "../jd.config";

export function HomeHeader() {
    

    return jd.div({className: "flex flex-col"},[
        jd.div({className: "h-20 w-full bg-amber-400"},[
            jd.div({className: " h-full container flex flex-row items-center justify-between m-auto"},[
                jd.img({className: "h-30" ,src:"/assets/LumacaExpress_logo.png"}),
                jd.div({ className: "flex flex-row gap-2"},[
                    jd.a({className: "btn btn-lg bg-amber-300 btn-ghost", href: "/register"}, ["Sign up"]),
                    jd.a({className: "btn btn-lg bg-amber-300 btn-ghost", href: "/login"}, ["Log in"])   
                ]) 
            ])
        ]),       
    ])
}