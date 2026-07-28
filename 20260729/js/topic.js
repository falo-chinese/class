/**
 * 天心 ERP 教學專區 - 獨立主題頁面通用腳本
 */

document.addEventListener('DOMContentLoaded', () => {
  // 自動生成側邊目錄 Table of Contents (TOC)
  const tocList = document.getElementById('tocList');
  const articleHeaders = document.querySelectorAll('.article-content h2, .article-content h3');

  if (tocList && articleHeaders.length > 0) {
    tocList.innerHTML = '';
    articleHeaders.forEach((header, idx) => {
      if (!header.id) {
        header.id = `heading-${idx}`;
      }

      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = `#${header.id}`;
      a.className = 'toc-link';
      a.textContent = header.textContent;
      
      if (header.tagName.toLowerCase() === 'h3') {
        a.style.paddingLeft = '1.25rem';
        a.style.fontSize = '0.8rem';
      }

      li.appendChild(a);
      tocList.appendChild(li);
    });
  }

  // 標記該文章閱讀狀態按鈕
  const markCompleteBtn = document.getElementById('markCompleteBtn');
  const pageTopicId = document.body.dataset.topicId;

  if (markCompleteBtn && pageTopicId) {
    function updateBtnState() {
      const completedTopics = JSON.parse(localStorage.getItem('erp_completed_topics') || '[]');
      if (completedTopics.includes(pageTopicId)) {
        markCompleteBtn.innerHTML = '✓ 已完成此主題學習';
        markCompleteBtn.style.background = 'var(--accent-emerald)';
        markCompleteBtn.style.color = '#fff';
      } else {
        markCompleteBtn.innerHTML = '○ 標記為完成學習';
        markCompleteBtn.style.background = 'rgba(59, 130, 246, 0.2)';
        markCompleteBtn.style.color = 'var(--accent-blue)';
      }
    }

    updateBtnState();

    markCompleteBtn.addEventListener('click', () => {
      let completedTopics = JSON.parse(localStorage.getItem('erp_completed_topics') || '[]');
      if (completedTopics.includes(pageTopicId)) {
        completedTopics = completedTopics.filter(id => id !== pageTopicId);
      } else {
        completedTopics.push(pageTopicId);
      }
      localStorage.setItem('erp_completed_topics', JSON.stringify(completedTopics));
      updateBtnState();
    });
  }
});
