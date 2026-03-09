const SIDEBAR = document.getElementById("wiki-sidebar")
const CONTENT = document.getElementById("wiki-content")

const WIKI_PATH = "wiki/"

async function loadManifest() {
    const res = await fetch(WIKI_PATH + "manifest.json")
    return await res.json()
}

function getPage() {
    const params = new URLSearchParams(location.search)
    return params.get("page")
}

function navigate(page) {
    history.pushState(null, null, "?page=" + encodeURIComponent(page))
    loadPage(page)
    highlight(page)
}

function isExternalLink(value) {
    return /^(https?:|mailto:|tel:|#|\/)/i.test(value)
}

function fixRelativePaths(container, page) {
    const pageDir = WIKI_PATH

    container.querySelectorAll("img").forEach(img => {
        const src = img.getAttribute("src")
        if (!src || isExternalLink(src)) {
            return
        }

        img.setAttribute("src", pageDir + src)
    })

    container.querySelectorAll("a").forEach(link => {
        const href = link.getAttribute("href")
        if (!href || isExternalLink(href)) {
            return
        }

        if (href.endsWith(".md")) {
            link.setAttribute("href", "?page=" + encodeURIComponent(href))
            link.addEventListener("click", (e) => {
                e.preventDefault()
                navigate(href)
            })
            return
        }

        link.setAttribute("href", pageDir + href)
    })
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
        fixRelativePaths(CONTENT, page)
    } catch {
        CONTENT.innerHTML = "<h2>Page not found</h2>"
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

async function init() {
    const manifest = await loadManifest()

    buildSidebar(manifest)

    let page = getPage()

    if (!page) {
        page = manifest[0].pages[0].file
    }

    await loadPage(page)
    highlight(page)
}

window.addEventListener("popstate", async () => {
    let page = getPage()

    if (!page) {
        const manifest = await loadManifest()
        page = manifest[0].pages[0].file
    }

    await loadPage(page)
    highlight(page)
})

init()