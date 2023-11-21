const filterOptions = document.querySelectorAll('.filter button')
const filterName = document.querySelector('.filter-info .name')
const filterValue = document.querySelector('.filter-info .value')
const filterSlider = document.querySelector('.slider input')
const rotateOptions = document.querySelectorAll('.rotate button')
const previewImg = document.querySelector('.preview-img img')
const resetFilterBtn = document.querySelector('.reset-filter')
const saveImgBtn = document.querySelector('.save-img')


let saturation = 100, inversion = 0, grayscale = 0
let rotate = 0, flipHorizontal = 1, filpVertical = 1

const applyFilters = () =>{
    previewImg.style.transform = `rotate(${rotate}deg) scale(${flipHorizontal}, ${filpVertical})`
    previewImg.style.filter = `saturate(${saturation}%) invert(${inversion}%) grayscale(${grayscale}%)`
}

filterOptions.forEach(option =>{
    option.addEventListener("click", ()=>{
        document.querySelector(".filter .active").classList.remove("active")
        option.classList.add("active")
        filterName.innerHTML = option.innerHTML

        if(option.id === "saturation"){
            filterSlider.max = '200'
            filterSlider.value = saturation
            filterValue.innerHTML = `${saturation}%`
        } else if(option.id === "inversion"){
            filterSlider.max = '100'
            filterSlider.value = inversion
            filterValue.innerHTML = `${inversion}%`
        }else{
            filterSlider.max = '100'
            filterSlider.value = grayscale
            filterValue.innerHTML = `${grayscale}%`
        }
    })
})

const updateFilter = () =>{
    filterValue.innerHTML = `${filterSlider.value}%`
    const selectedFilter = document.querySelector('.filter .active')

    if(selectedFilter.id === "saturation"){
        saturation = filterSlider.value
    }else if(selectedFilter.id === "inversion"){
        inversion = filterSlider.value
    }else{
        grayscale = filterSlider.value
    }

    applyFilters()
}

rotateOptions.forEach(option =>{
    option.addEventListener("click", ()=>{
        if(option.id === "left"){
            rotate -= 90;
        } else if(option.id === "right"){
            rotate += 90;
        } else if(option.id === "horizontal"){
            flipHorizontal = flipHorizontal === 1 ? -1: 1
        }else{
            filpVertical = filpVertical === 1 ? -1: 1
        }
        applyFilters()
    })
})

const resetFilter = () =>{
    saturation = 100, inversion = 0, grayscale = 0
    rotate = 0, flipHorizontal = 1, filpVertical = 1
    filterOptions[0].click()
    applyFilters()
}

const saveImg = () =>{
    const canvas = document.createElement("canvas")
    const ctx  = canvas.getContext("2d")
    canvas.width = previewImg.naturalWidth
    canvas.height = previewImg.naturalHeight

    ctx.filter = `saturate(${saturation}%) invert(${inversion}%) grayscale(${grayscale}%)`
    ctx.translate(canvas.width / 2, canvas.height / 2)
    if(rotate !== 0){
        ctx.rotate(rotate * Math.PI / 180)
    }
    ctx.scale(flipHorizontal, filpVertical)
    ctx.drawImage(previewImg, 0, 0, canvas.width, canvas.height)
    document.body.appendChild(canvas)
}



saveImgBtn.addEventListener("click", saveImg)
filterSlider.addEventListener("input", updateFilter)
resetFilterBtn.addEventListener("click", resetFilter)