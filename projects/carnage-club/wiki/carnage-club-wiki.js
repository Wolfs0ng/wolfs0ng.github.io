const SIDEBAR = document.getElementById("wiki-sidebar")
const CONTENT = document.getElementById("wiki-content")

const MOBILE_TOGGLE = document.getElementById("wiki-mobile-toggle")
const OVERLAY = document.getElementById("wiki-sidebar-overlay")

const LIGHTBOX = document.getElementById("wiki-lightbox")
const LIGHTBOX_MEDIA = document.getElementById("wiki-lightbox-media")
const LIGHTBOX_CLOSE = document.getElementById("wiki-lightbox-close")

const WIKI_PATH = "wiki/"

async function loadManifest() {
    const res = await fetch(WIKI_PATH + "manifest.json")
    return await res.json()
}

function getPage() {
    const params = new URLSearchParams(location.search)
    return params.get("page")
}

function closeMobileSidebar() {
    SIDEBAR.classList.remove("open")
    OVERLAY.classList.remove("visible")
}

function openMobileSidebar() {
    SIDEBAR.classList.add("open")
    OVERLAY.classList.add("visible")
}

function navigate(page) {
    history.pushState(null, null, "?page=" + encodeURIComponent(page))
    loadPage(page)
    highlight(page)
    closeMobileSidebar()
}

function isExternalLink(value) {
    return /^(https?:|mailto:|tel:|#|\/)/i.test(value)
}

function isMdFile(value) {
    return /\.md($|[?#])/i.test(value)
}

function isSvg(value) {
    return /\.svg($|[?#])/i.test(value)
}

function fixRelativePaths(container) {
    container.querySelectorAll("img").forEach(img => {
        const src = img.getAttribute("src")
        if (!src || isExternalLink(src)) {
            return
        }

        img.setAttribute("src", WIKI_PATH + src)
    })

    container.querySelectorAll("a").forEach(link => {
        const href = link.getAttribute("href")
        if (!href || isExternalLink(href)) {
            return
        }

        if (isMdFile(href)) {
            link.setAttribute("href", "?page=" + encodeURIComponent(href))
            link.addEventListener("click", (e) => {
                e.preventDefault()
                navigate(href)
            })
            return
        }

        link.setAttribute("href", WIKI_PATH + href)
    })
}

function createLightboxMedia(src, alt) {
    if (isSvg(src)) {
        const object = document.createElement("object")
        object.setAttribute("data", src)
        object.setAttribute("type", "image/svg+xml")
        object.setAttribute("aria-label", alt || "SVG preview")
        return object
    }

    const img = document.createElement("img")
    img.src = src
    img.alt = alt || ""
    return img
}

function initImageLightbox() {
    CONTENT.querySelectorAll("img").forEach(img => {
        img.addEventListener("click", () => {
            LIGHTBOX_MEDIA.innerHTML = ""
            LIGHTBOX_MEDIA.appendChild(createLightboxMedia(img.src, img.alt || ""))
            LIGHTBOX.hidden = false
            document.body.style.overflow = "hidden"
        })
    })
}

function closeLightbox() {
    LIGHTBOX.hidden = true
    LIGHTBOX_MEDIA.innerHTML = ""
    document.body.style.overflow = ""
}

function initMobileSidebar() {
    if (!MOBILE_TOGGLE) {
        return
    }

    MOBILE_TOGGLE.addEventListener("click", () => {
        openMobileSidebar()
    })

    OVERLAY.addEventListener("click", () => {
        closeMobileSidebar()
    })
}

function setActiveLangButton(lang) {
    const buttons = document.querySelectorAll(".lang-btn")
    buttons.forEach(button => {
        const isActive = button.dataset.lang === lang
        button.setAttribute("aria-pressed", isActive ? "true" : "false")
        button.classList.toggle("is-active", isActive)
    })
}

function initLanguageButtons() {
    const buttons = document.querySelectorAll(".lang-btn")
    if (!buttons.length) {
        return
    }

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            const lang = button.dataset.lang
            if (!lang) {
                return
            }

            localStorage.setItem("lang", lang)

            if (typeof window.setLanguage === "function") {
                window.setLanguage(lang)
            } else if (typeof window.applyLanguage === "function") {
                window.applyLanguage(lang)
            } else {
                document.querySelectorAll("[data-i18n]").forEach(node => {
                    const nodeLang = node.getAttribute("data-i18n")
                    node.hidden = nodeLang !== lang
                })
            }

            setActiveLangButton(lang)
        })
    })

    const currentLang = localStorage.getItem("lang") || "ua"

    if (typeof window.setLanguage === "function") {
        window.setLanguage(currentLang)
    } else if (typeof window.applyLanguage === "function") {
        window.applyLanguage(currentLang)
    } else {
        document.querySelectorAll("[data-i18n]").forEach(node => {
            const nodeLang = node.getAttribute("data-i18n")
            node.hidden = nodeLang !== currentLang
        })
    }

    setActiveLangButton(currentLang)
}

async function loadPage(page) {
    try {
        const res = await fetch(WIKI_PATH + page)

        if (!res.ok) {
            throw new Error("404")
        }

        const md = await res.text()
        const html = DOMPurify.sanitize(marked.parse(md))

        CONTENT.innerHTML = html

        fixRelativePaths(CONTENT)
        initImageLightbox()
        closeMobileSidebar()
    } catch {
        CONTENT.innerHTML = "<h2>Page not found</h2>"
        closeMobileSidebar()
    }
}

function highlight(page) {
    document.querySelectorAll(".sidebar-link").forEach(link => {
        link.classList.remove("active")

        if (link.dataset.page === page) {
            link.classList.add("active")
        }
    })
}

function buildSidebar(data) {
    SIDEBAR.innerHTML = ""

    data.forEach(section => {
        const block = document.createElement("div")
        block.className = "sidebar-section"

        const title = document.createElement("div")
        title.className = "sidebar-title"
        title.textContent = section.section

        block.appendChild(title)

        section.pages.forEach(p => {
            const link = document.createElement("a")

            link.className = "sidebar-link"
            link.textContent = p.title
            link.href = "?page=" + encodeURIComponent(p.file)
            link.dataset.page = p.file

            link.onclick = (e) => {
                e.preventDefault()
                navigate(p.file)
            }

            block.appendChild(link)
        })

        SIDEBAR.appendChild(block)
    })
}

LIGHTBOX_CLOSE.addEventListener("click", closeLightbox)

LIGHTBOX.addEventListener("click", (e) => {
    if (e.target === LIGHTBOX) {
        closeLightbox()
    }
})

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !LIGHTBOX.hidden) {
        closeLightbox()
    }

    if (e.key === "Escape") {
        closeMobileSidebar()
    }
})

window.addEventListener("popstate", async () => {
    let page = getPage()

    if (!page) {
        const manifest = await loadManifest()
        page = manifest[0].pages[0].file
    }

    await loadPage(page)
    highlight(page)
})

async function init() {
    const manifest = await loadManifest()

    buildSidebar(manifest)
    initMobileSidebar()
    initLanguageButtons()

    let page = getPage()

    if (!page) {
        page = manifest[0].pages[0].file
    }

    await loadPage(page)
    highlight(page)
}

init()