import { HomeHeader } from "../components/home-header";
import { jd } from "../jd.config";

export function HomePage() {
    
    return jd.div({className:"flex flex-col"},[
        HomeHeader(),
        jd.img({className: "h-200 w-full object-cover object-top",src:"./assets/homepage.png"},[])
    ])
}