from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.models import Preset, Tag
from app.forms import PresetForm

presets_bp = Blueprint('presets', __name__)

@presets_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
      form = PresetForm()
      if form.validate_on_submit():
                preset = Preset(
                              title=form.title.data,
                              description=form.description.data,
                              content=form.content.data,
                              images=form.images.data,
                              is_public=form.is_public.data,
                              author=current_user
                )
                if form.tags.data:
                              tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
                              for name in tag_names:
                                                tag = Tag.query.filter_by(name=name).first()
                                                if not tag:
                                                                      tag = Tag(name=name)
                                                                      db.session.add(tag)
                                                                  preset.tags.append(tag)
                                        db.session.add(preset)
                          db.session.commit()
                flash('Preset created successfully!', 'success')
                return redirect(url_for('presets.view', id=preset.id))
            return render_template('presets/create.html', title='Create Preset', form=form)

@presets_bp.route('/<int:id>')
def view(id):
      preset = Preset.query.get_or_404(id)
    if not preset.is_public and preset.author != current_user:
              abort(403)
          return render_template('presets/view.html', title=preset.title, preset=preset)

@presets_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
      preset = Preset.query.get_or_404(id)
    if preset.author != current_user:
              abort(403)
          form = PresetForm()
    if form.validate_on_submit():
              preset.title = form.title.data
              preset.description = form.description.data
              preset.content = form.content.data
              preset.images = form.images.data
              preset.is_public = form.is_public.data
              preset.tags = []
              if form.tags.data:
                            tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
                            for name in tag_names:
                                              tag = Tag.query.filter_by(name=name).first()
                                              if not tag:
                                                                    tag = Tag(name=name)
                                                                    db.session.add(tag)
                                                                preset.tags.append(tag)
                                      db.session.commit()
                        flash('Preset updated!', 'success')
        return redirect(url_for('presets.view', id=preset.id))
elif request.method == 'GET':
        form.title.data = preset.title
        form.description.data = preset.description
        form.content.data = preset.content
        form.images.data = preset.images
        form.is_public.data = preset.is_public
        form.tags.data = ', '.join([t.name for t in preset.tags])
    return render_template('presets/create.html', title='Edit Preset', form=form, legend='Edit Preset')

@presets_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
      preset = Preset.query.get_or_404(id)
    if preset.author != current_user:
              abort(403)
    db.session.delete(preset)
    db.session.commit()
    flash('Preset has been deleted!', 'success')
    return redirect(url_for('main.index'))

@presets_bp.route('/explore')
def explore():
      page = request.args.get('page', 1, type=int)
    query = request.args.get('q')
    if query:
              presets = Preset.query.filter(
                  Preset.is_public == True,
                  (Preset.title.contains(query) | Preset.description.contains(query))
    ).order_by(Preset.timestamp.desc()).paginate(page=page, per_page=9)
else:
        presets = Preset.query.filter_by(is_public=True)\
            .order_by(Preset.timestamp.desc())\
            .paginate(page=page, per_page=9)
    return render_template('presets/explore.html', presets=presets, query=query)

@presets_bp.route('/<int:id>/like', methods=['POST'])
@login_required
def like(id):
      preset = Preset.query.get_or_404(id)
    if preset in current_user.liked_presets:
              current_user.liked_presets.remove(preset)
        flash('Unliked preset.', 'info')
else:
        current_user.liked_presets.append(preset)
        flash('Liked preset!', 'success')
    db.session.commit()
    return redirect(request.referrer or url_for('presets.view', id=id))

@presets_bp.route('/<int:id>/archive')
@login_required
def archive(id):
      preset = Preset.query.get_or_404(id)
    if preset.author != current_user:
              abort(403)
    preset.is_archived = not preset.is_archived
    db.session.commit()
    status = "archived" if preset.is_archived else "unarchived"
    flash(f'Preset {status}.', 'success')
    return redirect(url_for('presets.view', id=id))
