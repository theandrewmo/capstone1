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

    $('.find-brewery').on('submit', async function(e) {
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
            $('.results').empty()
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
    })

    function renderBrewery(brewery) {
        $('#results-header').removeClass('d-none')
        $('.results').append(
            `<h5><a href='/breweries/${brewery.id}'>${brewery.name}</a></h5>
            <p>${brewery.city}, ${brewery.state}</p>`)
    
    }

})