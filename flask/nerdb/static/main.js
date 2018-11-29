document.addEventListener('DOMContentLoaded', function(e) {
    document.getElementById('search-text').addEventListener('keyup', search)
})

search = async ()=> {
    const max_for = 10
    const categories = 'character'
    const datasource = 'tranquility'
    const lang = 'en-us'
    const strict = 'false'
    const search_val = document.getElementById('search-text').value
    const url = 'https://esi.evetech.net/latest/search/?categories=' + categories + '&datasource=' + datasource + '&language=' + lang + '&search=' + search_val + '&strict=' + strict
    const headers = {'User-Agent':'NERDb', 'Maintainer':'robertinthecloud@icloud.com'}

    let res = await fetch(url, {
        method: 'GET'
    })
    .then(response => response.json());
    
    let chars = []
    for (let i = 0; i < max_for; i++){
        if (res['character'][i]){
            let name = await get_name(res['character'][i])
            let char = {id: res['character'][i], name: name}
            chars.push(char)
        }
    }
    populate_element(chars, 'search-results')
}

function populate_element(chars, element) {
    let parent_div = document.getElementById(element)
    parent_div.innerHTML = ''

    for (i in chars){
        let link = document.createElement('a')
        let name_div = document.createElement('div')
        let name = document.createTextNode(chars[i].name)
        let portrait = document.createElement('img')
        link.setAttribute('href', 'character/' + chars[i].id)
        link.setAttribute('class', 'result-row')
        name_div.setAttribute('class', 'name-div')
        portrait.setAttribute('src', 'https://image.eveonline.com/Character/' + chars[i].id + '_64.jpg')

        link.appendChild(portrait)
        link.appendChild(name_div)
        name_div.appendChild(name)
        parent_div.appendChild(link)
    }
}

get_name = async (char_id)=> {
    const url = 'https://esi.evetech.net/latest/characters/' + char_id + '/?datasource=tranquility'

    let res = await fetch(url, {
        method: 'GET'
    })
    .then(response => response.json());

    return res['name']
}

function open_page(e) {
    console.log(e)
}
