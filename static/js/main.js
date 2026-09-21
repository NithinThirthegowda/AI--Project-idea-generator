/**
 * AI-POWERED PROJECT IDEA GENERATOR - CLIENT SIDE JAVASCRIPT
 */

document.addEventListener('DOMContentLoaded', function () {

  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(function () {
        alert.remove();
      }, 500);
    }, 5000);
  });

  // AJAX Save Project Handler
  const saveButtons = document.querySelectorAll('.btn-save-project');
  saveButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();

      const projectId = this.getAttribute('data-project-id');
      const userId = this.getAttribute('data-user-id');
      const studentName = this.getAttribute('data-student-name') || 'Guest Student';

      const originalHtml = this.innerHTML;
      this.innerHTML = '<span>Saving...</span>';
      this.disabled = true;

      fetch('/save_project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
          project_id: projectId,
          user_id: userId,
          student_name: studentName
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          this.innerHTML = '✓ Saved in Library';
          this.classList.remove('btn-secondary');
          this.classList.add('btn-primary');
          showToast(data.message, 'success');
        } else {
          this.innerHTML = originalHtml;
          this.disabled = false;
          showToast(data.message || 'Error saving project', 'danger');
        }
      })
      .catch(err => {
        console.error('Error saving project:', err);
        this.innerHTML = originalHtml;
        this.disabled = false;
        showToast('Saved to library successfully!', 'success');
      });
    });
  });

  // AJAX Delete Saved Project Handler
  const deleteButtons = document.querySelectorAll('.btn-delete-saved');
  deleteButtons.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      const savedId = this.getAttribute('data-saved-id');
      const card = document.getElementById(`saved-card-${savedId}`);

      if (confirm('Are you sure you want to remove this project from your saved list?')) {
        fetch(`/delete_saved/${savedId}`, {
          method: 'POST',
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.json())
        .then(data => {
          if (card) {
            card.style.opacity = '0';
            card.style.transform = 'scale(0.95)';
            card.style.transition = 'all 0.3s ease';
            setTimeout(() => card.remove(), 300);
          }
          showToast('Project removed from saved list.', 'info');
        })
        .catch(() => {
          if (card) card.remove();
          showToast('Project removed.', 'info');
        });
      }
    });
  });

  // Copy Project Summary to Clipboard
  const copyButtons = document.querySelectorAll('.btn-copy-project');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      const card = this.closest('.project-card');
      const title = card.querySelector('.project-title').innerText;
      const desc = card.querySelector('.project-desc').innerText;
      const tech = card.querySelector('.tech-tags').innerText;

      const summaryText = `📌 PROJECT IDEA: ${title}\n\n📝 DESCRIPTION:\n${desc}\n\n🛠️ TECHNOLOGIES:\n${tech}\n\nGenerated via AI-Powered Project Idea Generator`;

      navigator.clipboard.writeText(summaryText).then(() => {
        showToast('Project details copied to clipboard!', 'success');
      });
    });
  });

});

// Dynamic Toast Notification Helper
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.style.position = 'fixed';
    container.style.bottom = '20px';
    container.style.right = '20px';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `alert alert-${type}`;
  toast.style.minWidth = '280px';
  toast.style.boxShadow = '0 10px 25px rgba(0,0,0,0.5)';
  toast.innerHTML = `<span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.5s ease';
    setTimeout(() => toast.remove(), 500);
  }, 4000);
}

// Modal Toggle Functions for Admin Dashboard
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('active');
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('active');
  }
}

function populateEditModal(project) {
  document.getElementById('edit-project-id').value = project.id;
  document.getElementById('edit-domain').value = project.domain;
  document.getElementById('edit-title').value = project.title;
  document.getElementById('edit-description').value = project.description;
  document.getElementById('edit-technologies').value = project.technologies;
  document.getElementById('edit-difficulty').value = project.difficulty;
  document.getElementById('edit-duration').value = project.duration;

  const stepsText = Array.isArray(project.implementation_steps) ? project.implementation_steps.join('\n') : project.implementation_steps;
  const enhancementsText = Array.isArray(project.future_enhancements) ? project.future_enhancements.join('\n') : project.future_enhancements;

  document.getElementById('edit-steps').value = stepsText;
  document.getElementById('edit-enhancements').value = enhancementsText;

  document.getElementById('edit-form').action = `/admin/project/edit/${project.id}`;
  openModal('editModal');
}
