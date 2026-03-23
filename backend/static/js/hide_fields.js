
document.addEventListener('change', function(e) {
    if (e.target.id.includes('content_type')) {
        let container = e.target.closest('.inline-related');
        let type = e.target.value;


        container.querySelector('.field-video_url').style.display = (type === 'VID') ? 'block' : 'none';
        container.querySelector('.field-file').style.display = (type === 'FILE') ? 'block' : 'none';
        container.querySelector('.field-external_link').style.display = (type === 'EX_LINK') ? 'block' : 'none';
    }
});