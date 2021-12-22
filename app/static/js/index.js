function selectSys(btnName) {
    let sysIframeList = document.getElementsByName("sys-iframe")
    sysIframeList.forEach(function (sysIframe) {
        sysIframe.style["display"] = "none"
        if (btnName + "-iframe" == sysIframe.getAttribute("id")) {
            sysIframe.style["display"] = "inline"
        }
    })
}

function selectFun() {
    let selectFun = document.getElementById("select-fun")
    let functionElements = document.getElementsByName("functions")
    // 获取被选中的索引
    let funX = selectFun.selectedIndex;
    functionElements.forEach(function (value, index) {
        let selectedFun = document.getElementById("fun" + index)
        if (funX == index) {
            selectedFun.style["display"] = "inline"
        } else {
            selectedFun.style["display"] = "none"
        }
    })
}

function close_flash_message() {
    let messageElement = document.getElementById("flash-message-id").close()
    let divMessageElement = document.getElementById("div-message-id")
    messageElement.removeAttribute('open')
    divMessageElement.style["display"] = "none"
    messageElement.close()
}