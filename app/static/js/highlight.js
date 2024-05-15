let isHighlight = localStorage.getItem('highlightChecked') !== 'false'; // default to true

function cancelBtnHandler() {
    cancelHighlighting();
    document.getElementById("text-content").removeEventListener("click", fillInWord, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillInWord, false);
    document.getElementById("text-content").addEventListener("click", fillInWord2, false);
    document.getElementById("text-content").addEventListener("touchstart", fillInWord2, false);
}

function showBtnHandler() {
    document.getElementById("text-content").removeEventListener("click", fillInWord2, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillInWord2, false);
    document.getElementById("text-content").addEventListener("click", fillInWord, false);
    document.getElementById("text-content").addEventListener("touchstart", fillInWord, false);
    highLight();
}

function getWord() {
    return window.getSelection ? window.getSelection() : document.selection.createRange().text;
}

function highLight() {
    if (!isHighlight) return;
    let articleContent = document.getElementById("article").innerHTML; // innerHTML保留HTML标签来保持部分格式，且适配不同的浏览器
    let pickedWords = document.getElementById("selected-words");  // words picked to the text area
    let dictionaryWords = document.getElementById("selected-words2"); // words appearing in the user's new words list
    let allWords = dictionaryWords === null ? pickedWords.value + " " : pickedWords.value + " " + dictionaryWords.value;
    const list = allWords.split(" "); // 将所有的生词放入一个list中
    let totalSet = new Set();
    for (let i = 0; i < list.length; ++i) {
        list[i] = list[i].replace(/(^\W*)|(\W*$)/g, ""); // 消除单词两边的非单词字符
        if (list[i] != "" && !totalSet.has(list[i])) {
            // 返回所有匹配单词的集合, 正则表达式RegExp()中, "\b"匹配一个单词的边界, g 表示全局匹配, i 表示对大小写不敏感。
            let matches = new Set(articleContent.match(new RegExp("\\b" + list[i] + "\\b", "gi")));
            if (matches.has("mark")) {
                // 优先处理单词为 "mark" 的情况
                totalSet = new Set(["mark", ...totalSet]);
            }
            totalSet = new Set([...totalSet, ...matches]);
        }
    }
    // 删除所有的mark标签,防止标签发生嵌套
    articleContent = articleContent.replace(/<(mark)[^>]*>/gi, "");
    articleContent = articleContent.replace(/<(\/mark)[^>]*>/gi, "");
    // 将文章中所有出现该单词word的地方改为："<mark>" + word + "<mark>"。
    for (let word of totalSet) {
        articleContent = articleContent.replace(new RegExp("\\b" + word + "\\b", "g"), "<mark>" + word + "</mark>");
    }
    document.getElementById("article").innerHTML = articleContent;
}

function cancelHighlighting() {
    let articleContent = document.getElementById("article").innerHTML;
    articleContent = articleContent.replace(/<(mark)[^>]*>/gi, "");
    articleContent = articleContent.replace(/<(\/mark)[^>]*>/gi, "");
    document.getElementById("article").innerHTML = articleContent;
}

function fillInWord() {
    highLight();
}

function fillInWord2() {
    cancelHighlighting();
}

function toggleHighlighting() {
    if (isHighlight) {
        isHighlight = false;
        cancelHighlighting();
    } else {
        isHighlight = true;
        highLight();
    }
     localStorage.setItem('highlightChecked', isHighlight);
}

showBtnHandler();