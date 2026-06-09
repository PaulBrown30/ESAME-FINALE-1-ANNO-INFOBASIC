import { AccountHeader } from "../components/accounts-header"
import { jd } from "../jd.config"
import { createSignal, effect } from "@just-dom/signals"
import { createRef } from "just-dom"
import { NoAccess } from "../components/no-access"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

// Fix marker icon con bundler
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png"
import markerIcon from "leaflet/dist/images/marker-icon.png"
import markerShadow from "leaflet/dist/images/marker-shadow.png"
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
})

// ─── Geocoding ────────────────────────────────────────────────────────────────

async function geocodeCAP(cap) {
    const res = await fetch(
        `https://nominatim.openstreetmap.org/search?postalcode=${cap}&country=IT&format=json&limit=1`
    )
    const data = await res.json()
    if (data.length > 0) {
        return { lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon), cap }
    }
    return null
}

// ─── Routing OSRM ─────────────────────────────────────────────────────────────

async function buildRoute(coords) {
    const coordString = coords.map(c => `${c.lng},${c.lat}`).join(";")
    const res = await fetch(
        `https://router.project-osrm.org/route/v1/driving/${coordString}?overview=full&geometries=geojson`
    )
    const data = await res.json()
    if (data.code !== "Ok" || !data.routes.length) return null
    return data.routes[0].geometry
}

// ─── Mappa ────────────────────────────────────────────────────────────────────

let _mapInstance = null

async function buildRouteMap(packages, courierCap) {
    const mapEl = document.getElementById("map")
    if (!mapEl) return

    // Distruggi istanza precedente
    if (_mapInstance) {
        _mapInstance.remove()
        _mapInstance = null
    }
    mapEl.innerHTML = ""

    const caps = []

    // Se nessun pacco è "In consegna" (S-002), aggiungi il cap del corriere come prima tappa
    const hasPackageInDelivery = packages.some(pkg =>
        pkg.statuses.some(s => s.id === "S-002")
    )

    if (!hasPackageInDelivery && courierCap) {
        caps.push({ cap: courierCap, label: "Posizione corriere", isSender: null })
    }

    // Costruisce la sequenza: mittente pacco1, destinatario pacco1, mittente pacco2, ...
    for (const pkg of packages) {
        caps.push({ cap: pkg.sender_cap,   label: `Mittente – ${pkg.sender_name} ${pkg.sender_surname}`,    isSender: true  })
        caps.push({ cap: pkg.receiver_cap, label: `Destinatario – ${pkg.receiver_name} ${pkg.receiver_surname}`, isSender: false })
    }

    // Geocodifica con delay per Nominatim
    const coords = []
    for (const item of caps) {
        const point = await geocodeCAP(item.cap)
        if (point) coords.push({ ...point, label: item.label, isSender: item.isSender })
        await new Promise(r => setTimeout(r, 250))
    }

    if (coords.length === 0) return

    _mapInstance = L.map("map").setView([coords[0].lat, coords[0].lng], 7)

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "© OpenStreetMap contributors"
    }).addTo(_mapInstance)

    // Routing reale su strada via OSRM
    const geometry = await buildRoute(coords)
    if (geometry) {
        L.geoJSON(geometry, {
            style: { color: "#f59e0b", weight: 4, opacity: 0.9 }
        }).addTo(_mapInstance)
    } else {
        // Fallback: linea d'aria se OSRM fallisce
        const latlngs = coords.map(c => [c.lat, c.lng])
        L.polyline(latlngs, {
            color: "#f59e0b",
            weight: 3,
            dashArray: "8, 6",
            opacity: 0.85
        }).addTo(_mapInstance)
    }

    // Marker personalizzati
    coords.forEach((point, i) => {
        const isCourier = point.isSender === null
        const color = isCourier ? "#6366f1" : point.isSender ? "#f59e0b" : "#10b981"

        const icon = L.divIcon({
            className: "",
            html: `<div style="
                background: ${color};
                color: white;
                font-size: 11px;
                font-weight: 700;
                border-radius: 50%;
                width: 28px;
                height: 28px;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 2px solid white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.25);
            ">${isCourier ? "🚚" : i + 1}</div>`,
            iconSize: [28, 28],
            iconAnchor: [14, 14],
            popupAnchor: [0, -16]
        })

        const popupIcon = isCourier ? "🚚 Corriere" : point.isSender ? "📦 Mittente" : "🏠 Destinatario"

        L.marker([point.lat, point.lng], { icon })
            .addTo(_mapInstance)
            .bindPopup(`
                <div style="font-family:sans-serif;font-size:13px;min-width:160px">
                    <b style="color:${color}">${popupIcon}</b><br/>
                    ${point.label}<br/>
                    <span style="color:#888">CAP: ${point.cap}</span>
                </div>
            `)
    })

    // Adatta la vista a tutti i punti
    const latlngs = coords.map(c => [c.lat, c.lng])
    _mapInstance.fitBounds(latlngs, { padding: [24, 24] })
}

// ─── Pagina ───────────────────────────────────────────────────────────────────

export function CourierPage() {

    const courier_id = location.pathname.replace("/couriers/", "")

    const [CourierPackages, SetCourierPackages] = createSignal([])
    const [CourierData, SetCourierData] = createSignal()
    const [Loading, SetLoading] = createSignal(false)
    const inputRef = createRef()

    const token = localStorage.getItem("token")

    fetch(`http://127.0.0.1:5000/api/couriers/${courier_id}`, {
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    })
    .then(async (res) => {
        SetLoading(true)
        const courier_data = await res.json()
        const packages = courier_data.packages
        if (res.ok) {
            SetCourierData(courier_data)
            SetCourierPackages(packages)
        }
    })
    .catch((err) => console.log(err))
    .finally(() => SetLoading(false))

    function HandleAddStatus(status_id) {
        SetLoading(true)
        fetch(`http://127.0.0.1:5000/api/packages/${CourierPackages()[0].id}/add_status`, {
            method: "POST",
            body: JSON.stringify({ "status_id": status_id, "courier_id": parseInt(courier_id) }),
            headers: { "Content-Type": "application/json" },
        })
        .then(async (res) => {
        SetLoading(true)
        const courier_data = await res.json()
        const packages = courier_data.packages
        if (res.ok) {
            SetCourierData(courier_data)
            SetCourierPackages(packages)
        }
    })
    .catch((err) => console.log(err))
    .finally(() => SetLoading(false))

    }

    return jd.div({}, [
        jd.table({
            className: "flex flex-col w-full h-screen bg-amber-200",
            ref: (el) => {
                effect(el, () => {
                    if (CourierData()) {
                        el.replaceChildren(
                            AccountHeader(),
                            jd.tbody({
                                className: "container self-center mt-4",
                                ref: (el) => {
                                    effect(el, () => {
                                        if (!Loading()) {
                                            el.innerHTML = ""
                                            el.append(
                                                jd.div({ className: "flex flex-row my-4 gap-4" }, [
                                                    // Card corriere
                                                    jd.div({
                                                        className: "flex flex-col px-6 py-3 bg-white rounded-xl",
                                                    }, [
                                                        jd.p({ className: "font-bold" }, ["Corriere:"]),
                                                        jd.p({
                                                            className: "",
                                                            ref: (el) => {
                                                                effect(el, () => {
                                                                    if (CourierData()) {
                                                                        el.textContent = `${CourierData().name} ${CourierData().surname} / Cap  ${CourierData().current_cap}`
                                                                    }
                                                                })
                                                            },
                                                        }, []),
                                                        jd.div({
                                                            className:"",
                                                            ref: el => {
                                                                effect(el, ()=> {
                                                                    if (CourierPackages()[0]) {
                                                                        el.replaceChildren(
                                                                            jd.div({className: "flex flex-col py-3 border-t gap-2"},[
                                                                                jd.p({},[`Cambia stato del pacco ${CourierPackages()[0].id}:`]),
                                                                                jd.button({className: "btn bg-amber-400 text-white "+ (CourierPackages()[0].statuses.some(s => s.id == "S-002")? "hidden":""),
                                                                                    onclick: () => {HandleAddStatus("S-002")}
                                                                                  },["Ritirato"]),
                                                                                jd.button({className: "btn bg-amber-400 text-white "+ (!CourierPackages()[0].statuses.some(s => s.id == "S-002")? "hidden":""),
                                                                                    onclick: () => {HandleAddStatus("S-003")}
                                                                                },["Consegnato"]),
                                                                                jd.button({className: "btn bg-red-400 text-white "+ (!CourierPackages()[0].statuses.some(s => s.id == "S-002")? "hidden":""),
                                                                                    onclick: () => {HandleAddStatus("S-101")}
                                                                                },["Non Consegnato"]),
                                                                                jd.button({className: "btn bg-red-400 text-white "+ (!CourierPackages()[0].statuses.some(s => s.id == "S-002")? "hidden":""),
                                                                                    onclick: () => {HandleAddStatus("S-102")}
                                                                                },["Smarrito"]),
                                                                                jd.button({className: "btn bg-red-400 text-white "+ (CourierPackages()[0].statuses.some(s => s.id == "S-002")? "hidden":""),
                                                                                    onclick: () => {HandleAddStatus("S-103")}
                                                                                },["Non Trovato/Ritirato"]),
                                                                            ])
                                                                        )
                                                                    }
                                                                })
                                                            }
                                                        },[])
                                                    ]),
                                                    // Contenitore mappa
                                                    jd.div({
                                                        id: "map",
                                                        style: "height:300px; flex:1; border-radius:12px; overflow:hidden; background:#fef3c7; min-width:300px;",
                                                    }, []),
                                                ])
                                            )

                                            // Aspetta che #map sia nel DOM, poi costruisce la mappa
                                            setTimeout(() => {
                                                buildRouteMap(CourierPackages(), CourierData()?.current_cap)
                                            }, 0)

                                            el.append(
                                                ...CourierPackages().map((package_data,index) =>
                                                    packageRow({ package_data,index,courier: CourierData()})
                                                )
                                            )
                                        } else {
                                            el.replaceChildren(
                                                jd.lucide("Loader2", { className: "animate-spin size-10 mx-auto mt-10" })
                                            )
                                        }
                                    })
                                },
                            }, [])
                        )
                    } else {
                        el.replaceChildren(NoAccess())
                    }
                })
            },
        }, []),
    ])
}

// ─── Riga pacchetto ───────────────────────────────────────────────────────────

function packageRow({ package_data,index,courier }) {
    return jd.tr({
        className: "mt-4 shadow-xl bg-amber-100 rounded-2xl border-2 m-2 mx-6 gap-3",
    }, [
        jd.td({ className: "p-4 px-6 border-l-2 align-top" }, [
            jd.p({ className: "font-bold" }, ["Codice"]),
            jd.p({}, [`${package_data.id}`]),
        ]),
        jd.td({ className: "p-4 px-6 border-l-2 align-top" }, [
            jd.p({ className: "font-bold" }, ["Mittente"]),
            jd.p({}, [`${package_data.sender_name} ${package_data.sender_surname}`]),
            jd.p({}, [`CAP. ${package_data.sender_cap}`]),
            jd.div({className: " text-center border font-semibold bg-amber-400"},[(package_data.sender_cap == courier.current_cap && index == 0 && package_data.statuses.some(s => s.id == "S-002" ))?  "Posizione attuale": `Tappa n.${index * 2 + 1}`])
        ]),
        jd.td({ className: "p-4 px-6 border-l-2 align-top" }, [
            jd.p({ className: "font-bold" }, ["Destinatario"]),
            jd.p({}, [`${package_data.receiver_name} ${package_data.receiver_surname}`]),
            jd.p({}, [`CAP. ${package_data.receiver_cap}`]),
            jd.div({className: " text-center border font-semibold bg-amber-400"},[`Tappa n.${index * 2 + 2}`])
        ]),
        jd.td({ className: "p-4 px-6 border-l-2 align-top" }, [
            jd.p({ className: "font-bold" }, ["Peso"]),
            jd.p({}, [`${package_data.weight} kg.`]),
        ]),
        jd.td({ className: "p-4 px-6 border-l-2 align-top" }, [
            jd.p({ className: "font-bold" }, ["Data di arrivo stimata"]),
            jd.p({}, [`${package_data.estimated_arrival_date}`]),
        ]),
        jd.td({ className: "p-4 px-6 border-l-2 align-top" }, [
            jd.div({
                className: "flex flex-row relative justify-between bg-white py-3 px-2 rounded-2xl shadow-lg gap-6",
            }, [
                jd.div({
                    className:
                        "flex flex-col items-center " +
                        (package_data.statuses.some((s) => s.id === "S-001")
                            ? "text-amber-400"
                            : "opacity-20"),
                }, [
                    jd.lucide("PackageCheck", { className: "size-10" }),
                    jd.p({ className: "font-bold" }, ["Preso in Carico"]),
                ]),
                jd.div({
                    className:
                        "flex flex-col items-center " +
                        (package_data.statuses.some((s) => s.id === "S-002")
                            ? "text-amber-400"
                            : "opacity-20"),
                }, [
                    jd.lucide("Van", { className: "size-10" }),
                    jd.p({ className: "font-bold" }, ["In consegna"]),
                ]),
                jd.div({
                    className:
                        "flex flex-col items-center " +
                        (package_data.statuses.some((s) => s.id === "S-003")
                            ? "text-amber-400"
                            : "opacity-20"),
                }, [
                    jd.lucide("Home", { className: "size-10" }),
                    jd.p({ className: "font-bold" }, ["Consegnato"]),
                ]),
            ]),
        ]),
    ])
}