$(function() {

    /** base URL for brewery API */
    const base_url = `https://api.openbrewerydb.org/v1/breweries/`

    /** list of states used for search by state  */
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
        
    /** list of brewery types used for search by type  */
    const typeList = ['', 'micro', 'nano', 'regional', 'brewpub', 'large', 'planning',
        'bar', 'contract', 'proprietor']

    /** This function gets the users location from their browser
     *  if unsuccessful it will return an error message
     */

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

    /** helper function to process brewery API response data
     * takes response data and dataType as parameters, turns response data into an results object to be rendered
     * dataType is in regards to autocomplete or normal results
     */

    function processBreweries(data, dataType){
        const breweriesResults = Object.values(data).map((brewery) => {
            return createBrewery(brewery, dataType)
        })
        return breweriesResults;
    }

    /** adds click listener with grabItem callback function to the auto div, which will hold the autocomplete search results  */

    $('#auto').on('click', grabItem)

    /** add event listener for submission of the search form with callback function searchItem */

    $('.find-brewery').on('submit', searchItem)

    /** store timeout identifier */

 
    /** set up event handler for keyup on input field, checks whether search type is by keyword
     * calls debounced function runAutoComplete
     */

    $('#term').on('keyup', ()=> {
        if ($('#search_type').val() == 'by keyword') {
            debouncedRunAutoComplete()
        } 
    });

    /** debounce function that sets up debouncing on a passed in function */

    function debounce(func, delay = 500) {
        let timeoutId;
        return (...args) => {
            clearTimeout(timeoutId)
            timeoutId = setTimeout(()=> {
                func(...args)
            }, delay)
        }
    }

    /** assignment of the debounced function, in this case runAutoComplete  */

    const debouncedRunAutoComplete = debounce(runAutoComplete)

    /** helper function that appends the breweries data to a given element in the DOM */

    function renderBreweries(breweries, element) {
        $(element).empty().append(breweries)
    }

    /** readies DOM for results by changing display classes and emptying container of any old results */

    function readyForResults() {
        $('#recent-reviews').addClass('d-none')
        $('#results-header').removeClass('d-none')
        $('.results').empty()
    }        

    /** helper function that takes a brewery object as a parameter, creates and then returns a brewery DOM element. */

    function createBrewery(brewery, dataType) {
        let breweryElement;
        if (dataType == 'autoComplete') {
            breweryElement = $(`<p>${brewery.name}</p>`)
        }
        else {
             breweryElement = `<h5><a href='/breweries/${brewery.id}'>${brewery.name}</a></h5>
                <p>${brewery.city}, ${brewery.state}</p>`
            }
        return breweryElement
    }

    /** function for autocomplete, removes any existing results from DOM, requests new results from autocomplete endpoint based on seach term. */

    async function runAutoComplete(term) {
        try {
            $('#auto').empty()
            term = $('#term').val()
            const response = await axios({
                url: `${base_url}autocomplete`,
                method: "GET",
                params: {
                    query: term
                }
            })
            const breweries = processBreweries(response.data, 'autoComplete')
            renderBreweries(breweries, '#auto')
        }   
        catch(e) {
            console.error(e.message)
        }
    }

    /** function for getting the term the user has selected after attempting an autocomplete,
     *  updates input value to show user what they've selected 
     *  calls searchByKeyword in order to update the search results 
     */

    function grabItem(e) {
        $('#term').val(e.target.innerText)
        $('#auto').empty()
        readyForResults()
        searchByKeyword()
        $('#term').val('')
    }

    /** handling selections and searching */

    /** event handler for rendering the various input options depending on the type of search that is currently selected
     *  the callback function disables inputs when not relevant i.e. saved location, random brewery 
     *  renders additional input selectors from set options by calling renderSelector when appropriate i.e. by type, by state
     */

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

    /** function that renders additional selectors from global arrays for brewery type or state */

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

    /** asynchronous function that searches item:
     *  gathers the currently selected search type, (and term if relevant)
     */

    async function searchItem(e) {
        e.preventDefault();
        readyForResults();
        let term = ''
        let by_type = $('#search_type').val()
        let way_to_search = by_type.replace(/\s+/g, '_')
        if (way_to_search == 'by_distance') searchByDistance();
        else if (way_to_search == 'get_a_random_brewery') getRandomBrewery();
        else if (way_to_search == 'by_keyword') searchByKeyword();
        else {
            if (way_to_search == 'by_state' || way_to_search == 'by_type'){
                term = $('#choice').val()
            }
            else {
                term = $('#term').val()
                term = term.replace(/\s+/g, '_')
            
            }
            termSearch(way_to_search, term)
            $('#term').val('')
        }  
    }   

    /** asynchronous function for searching by keyword
     *  sends get request to API search endpoint
     */

    async function searchByKeyword() {
        try {
            term = $('#term').val()
            const response = await axios({
                url: `${base_url}search/`,
                method: "GET",
                params: {
                    query: term
                }
            })
            const breweries = processBreweries(response.data)
            renderBreweries(breweries, '.results')
        }
        catch(e) {
            console.error(e.message)
        }
    }

    /** asynchronous function for searching by distance 
     *  sends get request to API by_dist endpoint using location data saved in session
    */

    async function searchByDistance() {
        term = `${sessionStorage.getItem('latitude')},${sessionStorage.getItem('longitude')}`
        try {
            const response = await axios({
                url: `${base_url}`,
                method: "GET",
                params: {
                    by_dist: term
                }
            })
            const breweries = processBreweries(response.data)
            renderBreweries(breweries, '.results')
        }   
        catch(e) {
            console.error(e.message)
        }
    }

    /** asynchronous function for searching a random brewery
     *  sends get request to API "random" endpoint
    */

    async function getRandomBrewery() {
        try {
            const response = await axios({
                url: `${base_url}/random`,
                method: 'GET'
            })
            const breweries = processBreweries(response.data)
            renderBreweries(breweries, '.results')
        }
        catch(e) {
            console.error(e.message)
        }
    }

    /** asynchronous function for searching a brewery based on an input term (city, name, state, type)
     *  sends get request to API endpoint
    */

    async function termSearch(way_to_search, term) {
        try {
            const response = await axios({
                url: `${base_url}/`,
                method: "GET",
                params: {
                    [way_to_search]: term
                }
            })
            const breweries = processBreweries(response.data)
            renderBreweries(breweries, '.results')
        }   
        catch(e) {
            console.error(e.message)
        }
    }

    /** Mapping: uses google maps javascript API to render a map on brewery-details page */

    /** create map variable */
    let map;

    /** asynchronous function to initialize map object 
     * sets map location and marker based on latitude and longitude values present in the DOM 
     * if either value is not present i.e. location, then displays to user that no map is available
     */

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

    /** conditional that calls initMap when the window location is the brewery-detail page */

    if (window.location.href.match(/\/breweries\/[a-f0-9-]+$/)) {
        initMap();
      }

    /** check whether location is already stored in session, if not then calls function to get the location and store it
     * if geolocation not allowed, appropriate message is logged
     */

    if (!sessionStorage.getItem('latitude') && !sessionStorage.getItem('longitude') && 'geolocation' in navigator) {
        getLocation()
    }
    else if (sessionStorage.getItem('latitude') && sessionStorage.getItem('longitude')) {
        console.log('Location found in session')
    }
    else {
        console.log('Geolocation not enabled in this browser')
    }
})

