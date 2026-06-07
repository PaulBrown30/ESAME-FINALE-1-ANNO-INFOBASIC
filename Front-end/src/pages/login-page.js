import { jd } from "../jd.config"
import { createRef } from "just-dom"
import { createSignal } from "@just-dom/signals"
import { effect } from "@just-dom/signals"

export function LoginPage() {

    const passwordInputRef = createRef();
    const [PasswordVisible, SetPasswordVisible] = createSignal(false);
    const [Loading,SetLoading] = createSignal(false);

    const HandleSubmit = async (e) => {
        SetLoading(true)
        e.preventDefault()
        const dataform = new FormData(e.target)
        const data = Object.fromEntries(dataform)
        console.log(data)
        fetch(`http://127.0.0.1:5000/api/login`,
            {method: "POST",
            body: JSON.stringify(data),
            headers: {"Content-Type": "application/json"}
        })
        .then(async (res)=> {
            const data = await res.json()
            console.log(data)
            if (res.ok) {
                localStorage.setItem("token",data.token)
                location.pathname = `/${data.account.type}s/${data.account.id}`
            }
        })
        .catch((err)=> {
            console.log(err)
        })
        .finally(() => {
            SetLoading(false)
        })
    }

    return jd.div({className: "flex flex-col bg-amber-400 h-screen w-screen items-center justify-center"},[
        jd.img({className: "h-50" ,src:"/assets/LumacaExpress_logo.png"},[]),
        jd.form({
            className: "card w-100 shadow-2xl bg-amber-100",
            onsubmit: HandleSubmit
        },[
            jd.div({className: "card-body flex flex-col gap-3"},[
                jd.p({className: "text-2xl"},["Login"]),
                jd.div({},[
                    jd.label({className: "input validator w-full"},[
                        jd.lucide("Mail",{className:"size-5"}),
                        jd.input({
                            placeholder: "Inserisci email",
                            id: "email",
                            name: "email",
                            type: "email",
                            minLength: 3,
                            maxLength: 30,
                            pattern: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+[.][a-zA-Z]{2,}",
                            required: "true"
                        },[])
                    ]),
                    jd.p({className:"validator-hint hidden"},[
                        "Inserisci un email valida"
                    ])
                ]),
                jd.div({},[
                    jd.label({className: "input validator w-full"},[
                        jd.lucide("LockKeyhole",{className:"size-5"}),
                        jd.input({
                            ref: passwordInputRef,
                            placeholder: "Inserisci password",
                            id: "password",
                            name: "password",
                            type: "password",
                            minLength: 3,
                            maxLength: 30,
                            pattern: "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])[^ ]{8,}",
                            required: "true"
                        },[]),
                        jd.button({
                            className: `btn btn-xs`,
                            type: "button",
                            onclick: () => {
                                passwordInputRef.current.type = passwordInputRef.current.type == "password"? "text": "password";
                                SetPasswordVisible(PasswordVisible() == false ? true : false)
                            }
                        },[
                            jd.div({
                                ref: el => {
                                    effect(el, () => {
                                        if (PasswordVisible()) {
                                            el.replaceChildren(jd.lucide("Eye",{className:"size-5" },[]))
                                        } else {
                                            el.replaceChildren(jd.lucide("EyeClosed",{className:"size-5" },[]))
                                        }
                                    })
                                }
                            },[])
                        ]),
                    ]),
                    jd.p({className:"validator-hint hidden"},[
                        "Inserisci una password valida"
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
            },["Accedi"])
        ])
    ])
}