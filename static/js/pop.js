const btns = document.querySelectorAll(".btn");
const bg = document.getElementsByClassName("bg")[0]
const c = document.getElementsByClassName("close")[0]
btns.forEach((btn) => {
    btn.addEventListener("click", () => {
        bg.classList.contains("hide") ? bg.classList.remove("hide") : bg.classList.add("hide")
    })
})

c.addEventListener("click", () => {
    bg.classList.contains("hide") ? bg.classList.remove("hide") : bg.classList.add("hide")
})
