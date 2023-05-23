$(function() {

    const base_url = `https://api.openbrewerydb.org/v1/breweries/`

    
    const stateList = ["", "Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", 
        "California", "Colorado", "Connecticut", "District ", "of Columbia", 
        "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", 
        "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", 
        "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", 
        "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", 
        "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", 
        "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", 
        "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", 
        "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
        
    
    const typeList = ['', 'micro', 'nano', 'regional', 'brewpub', 'large', 'planning',
        'bar', 'contract', 'proprietor']
    
    function getLocation() {
        navigator.geolocation.getCurrentPosition(
            function success(position) {
                sessionStorage.setItem('latitude', position.coords.latitude);
                sessionStorage.setItem('longitude', position.coords.longitude);
            },
            function error(error_message) {
                console.error('An error has ocured', error_message)
            },
            {enableHighAccuracy: false}
        )
    }

    if (!sessionStorage.getItem('latitude') && !sessionStorage.getItem('longitude') && 'geolocation' in navigator) {
        getLocation()
    }
    else if (sessionStorage.getItem('latitude') && sessionStorage.getItem('longitude')) {
        console.log('Location found in session')
    }
    else {
        console.log('Geolocation not enabled in this browser')
    }

    let timeoutId;

    $('#term').on('keyup', ()=> {
        if ($('#search_type').val() == 'by keyword') {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(runAutocomplete, 500)
        } 
    });

    async function runAutocomplete(term) {
        $('#auto').remove()
        term = $('#term').val()
        try {
            const response = await axios({
                url: `${base_url}autocomplete`,
                method: "GET",
                params: {
                    query: term
                }
            })
            $('#term').after('<div id="auto"></div>')
            $('#auto').on('click', grabItem)
            Object.entries(response.data).forEach((entry) => {
                const [key, value] = entry;
                const brewery = value
                renderAutoComplete(brewery)
            })
        }   
        catch(e) {
            console.log(e.message)
        }
    }

    function grabItem(e) {
        $('#term').val(e.target.innerText)
        $('#auto').empty()
        searchByKeyword()
        $('#term').val('')
    }

    $('#search_type').on('change', (e) => {
        let selection = e.target.value
        if($('#choice')) {$('#choice').remove()}
        $('#term').removeAttr('disabled').val('').removeClass('d-none')
        if (selection == 'by distance') {
            $('#term').val(`Your saved location`)
            $('#term').attr('disabled','disabled')
        }
        else if (selection == 'get a random brewery') {
            $('#term').attr('disabled','disabled')}
        else if (selection == 'by type' || selection == 'by state') {
           renderSelector(selection)
        }
        else if(selection == 'by keyword'|| selection == 'by name' || selection == 'by city') {
            selection = selection.replace(/by /g, 'Enter a ');
            $('#term').attr('placeholder', selection)
        } 
    })

    function renderSelector(selection) {
        let termHTML = ''
        if (selection == 'by type') {
            termHTML = typeList.map(e => `<option value="${e}">${e}</option>`).join('')
        }
        else {
            termHTML = stateList.map(e => `<option value="${e}">${e}</option>`).join('')
        }
        let newSelector = `<select class="form-select text-center" id="choice" name="choice" placeholder="Search Type">
                            ${termHTML}
                            </select>`
        $('#term').after(newSelector).addClass('d-none')
    }

    async function searchItem(e) {
        e.preventDefault();
        $('#recent-reviews').addClass('d-none')
        let term = ''
        let by_type = $('#search_type').val()
        let way_to_search = by_type.replace(/\s+/g, '_')
        if (way_to_search !== 'by_keyword') {
            if (way_to_search == 'by_state' || way_to_search == 'by_type'){
                term = $('#choice').val()
            }
            else {
                term = $('#term').val()
                term = term.replace(/\s+/g, '_')
            }
            if (way_to_search == 'by_distance') {
                way_to_search = 'by_dist'
                term = `${sessionStorage.getItem('latitude')},${sessionStorage.getItem('longitude')}`

                try {
                    const response = await axios({
                        url: `${base_url}`,
                        method: "GET",
                        params: {
                            by_dist: term
                        }
                    })
                    $('.results').empty()

                    Object.entries(response.data).forEach((entry) => {
                        const [key, value] = entry;
                        const brewery = value
                        renderBrewery(brewery)
                    })
                }   
                catch(e) {
                console.log(e.message)
                }
            }
            else if (way_to_search == 'get_a_random_brewery') {
                try {
                    const response = await axios({
                        url: `${base_url}/random`,
                        method: 'GET'
                    })
                    $('.results').empty()
                    Object.entries(response.data).forEach((entry) => {
                        const [key, value] = entry;
                        const brewery = value
                        renderBrewery(brewery)
                    })
                }
                catch(e) {
                    console.log(e.message)
                }
            } 
            else {
                try {
                    const response = await axios({
                        url: `${base_url}/`,
                        method: "GET",
                        params: {
                            [way_to_search]: term
                        }
                    })
                    $('.results').empty()
                    $('#term').val('')
    
                    Object.entries(response.data).forEach((entry) => {
                        const [key, value] = entry;
                        const brewery = value
                        renderBrewery(brewery)
                    })
                }   
                catch(e) {
                    console.log(e.message)
                }
            }  
        }
        else {
             searchByKeyword()
            }   
    }   

    async function searchByKeyword() {
        $('.results').empty()
        $('#recent-reviews').addClass('d-none')
        term = $('#term').val()
        try {
            const response = await axios({
                url: `${base_url}search/`,
                method: "GET",
                params: {
                    query: term
                }
            })
            Object.entries(response.data).forEach((entry) => {
                const [key, value] = entry;
                const brewery = value
                renderBrewery(brewery)
            })
        }
        catch(e) {
            console.log(e.message)
        }
    }

    $('.find-brewery').on('submit', searchItem)

    function renderBrewery(brewery) {
        $('#results-header').removeClass('d-none')
        $('.results').append(
            `<h5><a href='/breweries/${brewery.id}'>${brewery.name}</a></h5>
            <p>${brewery.city}, ${brewery.state}</p>`)
    
    }

    function renderAutoComplete(brewery) {
            $('#auto').append(`<p>${brewery.name}</p>`)
    }

    let map;

    async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    let location = {lat: parseFloat($('#latitude').val()), lng: parseFloat($('#longitude').val())}
    if (location.lat && location.lng) {
        map = new Map($('#map')[0], {
            center: location,
            zoom: 12,
        });
        let marker = new google.maps.Marker({position:location, map:map})
    }
    else {
        $('#map').addClass('d-flex flex-column border border-primary border-2 align-items-center justify-content-center')
                .html(`<p>Unable to render map</p>
                       <p>Coordinates not available</p>
                    `)
    }}

    if (window.location.href.match(/\/breweries\/[a-f0-9-]+$/)) {
        initMap();
      }
    
})

