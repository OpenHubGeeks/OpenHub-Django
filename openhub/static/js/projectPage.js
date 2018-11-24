function getRequest(url, onSuccess) {
    $.get(url, function(data, status){
        onSuccess(data, status);
    });
}

function renderCard(project) {
    return `<div style="float: left;">
              <aside class="profile-card">
                  <header>
                    <a target="_blank" href="#">
                      <img src="${project.contributor && project.contributor.user_photo.url}" class="hoverZoomLink">
                    </a>
                    <h1>${project.project_name}</h1>
                    <h2>${project.project_techstack}</h2>
                  </header>
                  <div class="profile-bio">
                    <p>
                      ${project.project_description}
                    </p>
                  </div>
              </aside>
            </div>`;
}

function onSuccess(projects) {
    document.getElementById('app-content').innerHTML = projects.map(renderCard).join('');
};

function loadPage(pageNo) {
    getRequest(`/openhub/projects/?pageNo=${pageNo}`, onSuccess);
}

$(document).ready(function() {
    loadPage(1);
});