document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".service-title").forEach(title => {
        title.addEventListener("click", function() {
            let serviceId = this.dataset.serviceId;
            let list = document.getElementById(`service-${serviceId}`);
            list.classList.toggle("d-none");
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const minPriceInput = document.getElementById("min_price");
    const maxPriceInput = document.getElementById("max_price");
    const serviceLists = document.querySelectorAll('.lab-services-list');

    function getQueryParams() {
        const params = new URLSearchParams(window.location.search);
        return {
            minPrice: params.get("min_price"),
            maxPrice: params.get("max_price")
        };
    }

    const { minPrice, maxPrice } = getQueryParams();
    if (minPrice && maxPrice) {
        serviceLists.forEach(list => {
            list.classList.remove('d-none');
            list.classList.add('d-block');
        });
    }
});




