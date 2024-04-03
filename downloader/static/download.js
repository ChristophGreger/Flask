function download(sid) {

    /* Getting the form data */
    let video_url = document.getElementById("video_url").value;
    let selector = document.getElementById("quality_select");
    let video_quality = selector.options[selector.selectedIndex].value;

    /* Creating an anchor element to download the file */
    const anchor = document.createElement("a");
    anchor.href = `/download?video_url=${video_url}&quality_select=${video_quality}&sid=${sid}`;
    anchor.download = "";
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
}