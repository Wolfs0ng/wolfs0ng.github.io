const SIDEBAR = document.getElementById("wiki-sidebar")
const CONTENT = document.getElementById("wiki-content")

const WIKI_PATH = "wiki/"

async function loadManifest(){

const res = await fetch(WIKI_PATH + "manifest.json")

return await res.json()

}

function getPage(){

const params = new URLSearchParams(location.search)

return params.get("page")

}

function navigate(page){

history.pushState(null,null,"?page="+page)

loadPage(page)

highlight(page)

}

async function loadPage(page){

const res = await fetch(WIKI_PATH + page)

const md = await res.text()

const html = DOMPurify.sanitize(marked.parse(md))

CONTENT.innerHTML = html

}

function highlight(page){

document.querySelectorAll(".sidebar-link").forEach(link=>{

link.classList.remove("active")

if(link.dataset.page === page){

link.classList.add("active")

}

})

}

function buildSidebar(data){

SIDEBAR.innerHTML=""

data.forEach(section=>{

const block=document.createElement("div")
block.className="sidebar-section"

const title=document.createElement("div")
title.className="sidebar-title"
title.textContent=section.section

block.appendChild(title)

section.pages.forEach(p=>{

const link=document.createElement("a")

link.className="sidebar-link"

link.textContent=p.title

link.href="?page="+p.file

link.dataset.page=p.file

link.onclick=(e)=>{

e.preventDefault()

navigate(p.file)

}

block.appendChild(link)

})

SIDEBAR.appendChild(block)

})

}

async function init(){

const manifest=await loadManifest()

buildSidebar(manifest)

let page=getPage()

if(!page){

page=manifest[0].pages[0].file

}

loadPage(page)

highlight(page)

}

init()