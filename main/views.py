from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils.translation import activate
from .models import Project, AboutPage, ContactInfo

# НАСТРОЙКИ БРЕНДА
BRAND_NAME = "Aragats Antar"
BRAND_COLOR = "#0F7874"
HERO_IMAGE_URL = "/static/hero.jpg"


def set_language(request):
    lang = request.GET.get('lang', 'ru')
    if lang not in ['ru', 'en', 'hy']:
        lang = 'ru'
    activate(lang)
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('django_language', lang, max_age=31536000)
    return response


def get_language_switcher(current_lang):
    return f"""
    <div class="language-switcher">
        <a href="/set_lang/?lang=ru" class="lang-link {'active' if current_lang == 'ru' else ''}">РУС</a>
        <a href="/set_lang/?lang=en" class="lang-link {'active' if current_lang == 'en' else ''}">ENG</a>
        <a href="/set_lang/?lang=hy" class="lang-link {'active' if current_lang == 'hy' else ''}">ՀԱՅ</a>
    </div>
    """


def get_nav_links(current_page, t):
    links = [
        (t['home'], "/"),
        (t['about'], "/about/"),
        (t['projects'], "/#projects"),
        (t['map'], "/map/"),
        (t['join'], "/join/"),
    ]
    nav_html = ""
    for title, url in links:
        active = "active-link" if current_page == title else ""
        nav_html += f'<a href="{url}" class="{active}">{title}</a>'
    return nav_html


def get_footer_html(lang='ru'):
    from django.utils.translation import activate
    activate(lang)
    
    contact = ContactInfo.objects.first()
    
    address = contact.address if contact else _("Ереван, Армения")
    phone = contact.phone if contact else "+374 XX XXX XXX"
    email = contact.email if contact else "info@aragatsantar.am"
    description = contact.description if contact else _("Aragats Antar — восстанавливаем леса Армении для будущих поколений.")
    facebook = contact.facebook if contact else ""
    instagram = contact.instagram if contact else ""
    telegram = contact.telegram if contact else ""
    
    social_html = ""
    if facebook:
        social_html += f'<a href="{facebook}" target="_blank" class="social-link" title="Facebook"><svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z"/></svg></a>'
    if instagram:
        social_html += f'<a href="{instagram}" target="_blank" class="social-link" title="Instagram"><svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg></a>'
    if telegram:
        social_html += f'<a href="{telegram}" target="_blank" class="social-link" title="Telegram"><svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg></a>'
    
    footer_html = f"""
    <footer class="main-footer">
        <div class="footer-content">
            <div class="footer-col footer-about">
                <h3 class="footer-logo">{BRAND_NAME}</h3>
                <p class="footer-desc">{description}</p>
                <div class="social-links">{social_html}</div>
            </div>
            <div class="footer-col footer-links">
                <h4>{_("Навигация")}</h4>
                <a href="/">{_("Главная")}</a>
                <a href="/about/">{_("О нас")}</a>
                <a href="/#projects">{_("Проекты")}</a>
                <a href="/join/">{_("Присоединяйтесь")}</a>
            </div>
            <div class="footer-col footer-contacts">
                <h4>{_("Контакты")}</h4>
                <div class="contact-item">
                    <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-4.198 0-8 3.403-8 7.602 0 4.198 3.469 9.21 8 16.398 4.531-7.188 8-12.2 8-16.398 0-4.199-3.801-7.602-8-7.602zm0 11c-1.657 0-3-1.343-3-3s1.343-3 3-3 3 1.343 3 3-1.343 3-3 3z"/></svg>
                    <span>{address}</span>
                </div>
                <div class="contact-item">
                    <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M20 22.621l-3.521-6.795c-.008.004-1.974.97-2.064 1.011-2.24 1.086-6.799-7.82-4.609-8.994l2.083-1.026-3.493-6.817-2.106 1.039c-7.202 3.755 4.233 25.982 11.6 22.615.121-.055 2.102-1.029 2.11-1.033z"/></svg>
                    <a href="tel:{phone}">{phone}</a>
                </div>
                <div class="contact-item">
                    <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24"><path d="M0 3v18h24v-18h-24zm21.518 2l-9.518 7.713-9.518-7.713h19.036zm-19.518 14v-11.817l10 8.104 10-8.104v11.817h-20z"/></svg>
                    <a href="mailto:{email}">{email}</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2026 {BRAND_NAME}. {_("Все права защищены.")}</p>
        </div>
    </footer>
    """
    return footer_html


def home(request):
    lang = request.COOKIES.get('django_language', 'ru')
    if lang not in ['ru', 'en', 'hy']:
        lang = 'ru'
    activate(lang)
    
    t = {
        'home': _("Главная"), 'about': _("О нас"), 'projects': _("Проекты"), 'map': _("Карта"), 'join': _("Присоединяйтесь"),
        'hero_title': _("Каждое дерево — это шаг к будущему"),
        'how_to_help': _("Как вы можете помочь?"),
        'support_message': _("Мы масштабируемся и ищем единомышленников. Ваша поддержка критически важна для сохранения климата Армении."),
        'support_project': _("Поддержать проект"),
        'support': _("Поддержать"),
        'join_us': _("Присоединиться к нам"),
        'trees_planted': _("Посажено деревьев"),
        'no_projects': _("Пока нет активных проектов, но мы скоро начнем!"),
        'about_project': _("О проекте"), 'contacts': _("Контакты"),
    }

    projects = Project.objects.filter(is_active=True).order_by('-year')
    projects_html = ""
    
    for project in projects:
        images = project.images.all()
        slides_html = ""
        for idx, img in enumerate(images):
            slides_html += f'<div class="swiper-slide"><img src="{img.image.url}" alt="{project.title}" onclick="openLightbox(\'{img.image.url}\', {idx}, \'project-{project.id}\')"></div>'
        
        if len(images) > 1:
            image_html = f'<div class="swiper project-swiper" id="project-{project.id}"><div class="swiper-wrapper">{slides_html}</div><div class="swiper-button-prev"></div><div class="swiper-button-next"></div><div class="swiper-pagination"></div></div>'
        elif len(images) == 1:
            image_html = f'<div class="project-image">{slides_html}</div>'
        else:
            image_html = ""
            
        projects_html += f'<div class="project-card">{image_html}<div class="project-content"><h3>{project.title} <span style="font-size:0.8em; color:#666;">({project.year})</span></h3><p>{project.description}</p><div class="stat-badge"> {t["trees_planted"]}: {project.trees_planted}</div></div></div>'
    
    if not projects:
        projects_html = f"<p class='empty-msg'>{t['no_projects']}</p>"

    nav_links = get_nav_links(t['home'], t)
    lang_switcher = get_language_switcher(lang)
    footer_html = get_footer_html(lang)

    html = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{BRAND_NAME}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
        <style>
            :root {{ --brand: {BRAND_COLOR}; }}
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #FAFAFA; color: #333; line-height: 1.6; }}
            .main-header {{ position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; transition: all 0.4s ease-in-out; background-color: transparent; padding: 30px 0; }}
            .main-header.scrolled {{ background-color: white; box-shadow: 0 2px 15px rgba(0,0,0,0.08); padding: 15px 0; }}
            .header-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }}
            .logo-area {{ display: flex; align-items: center; gap: 20px; }}
            .logo-link {{ text-decoration: none; display: inline-block; transition: transform 0.3s ease; }}
            .logo-link:hover {{ transform: scale(1.05); }}
            .logo-img {{ height: 120px; width: auto; filter: brightness(0) invert(1) drop-shadow(0 2px 5px rgba(0,0,0,0.5)); transition: height 0.4s ease, filter 0.4s ease; }}
            .main-header.scrolled .logo-img {{ height: 70px; filter: none; }}
            nav {{ display: flex; align-items: center; gap: 20px; }}
            nav a {{ color: white; text-decoration: none; font-weight: 600; font-size: 1.05em; transition: opacity 0.2s; text-shadow: 0 2px 4px rgba(0,0,0,0.6); position: relative; }}
            .main-header.scrolled nav a {{ color: #333; text-shadow: none; }}
            nav a:hover {{ opacity: 0.7; }}
            nav a.active-link {{ opacity: 1; }}
            nav a.active-link::after {{ content: ''; position: absolute; bottom: -4px; left: 0; width: 100%; height: 2px; background-color: white; }}
            .main-header.scrolled nav a.active-link::after {{ background-color: var(--brand); }}
            .language-switcher {{ display: flex; gap: 5px; margin-left: 20px; padding-left: 20px; border-left: 1px solid rgba(255,255,255,0.3); }}
            .main-header.scrolled .language-switcher {{ border-left: 1px solid rgba(0,0,0,0.1); }}
            .lang-link {{ color: white; text-decoration: none; font-size: 0.9em; font-weight: bold; padding: 5px 8px; border-radius: 5px; transition: background 0.3s; }}
            .main-header.scrolled .lang-link {{ color: #333; }}
            .lang-link:hover, .lang-link.active {{ background: var(--brand); color: white !important; }}
            .hero {{ background: linear-gradient(rgba(15, 120, 116, 0.3), rgba(15, 120, 116, 0.25)), url('{HERO_IMAGE_URL}'); background-size: cover; background-position: center; height: 100vh; display: flex; align-items: center; justify-content: center; color: white; text-align: center; padding: 0 20px; }}
            .hero h2 {{ font-size: 4em; margin: 0; text-shadow: 0 4px 15px rgba(0,0,0,0.5); font-weight: 800; line-height: 1.2; }}
            .container {{ max-width: 900px; margin: 0 auto; padding: 60px 20px; }}
            h2.section-title {{ color: var(--brand); font-size: 2em; margin-bottom: 40px; position: relative; padding-bottom: 15px; }}
            h2.section-title::after {{ content: ''; position: absolute; bottom: 0; left: 0; width: 60px; height: 4px; background: var(--brand); }}
            .project-card {{ background: white; margin-bottom: 40px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); transition: transform 0.2s; overflow: hidden; }}
            .project-card:hover {{ transform: translateY(-5px); }}
            .project-swiper {{ width: 100%; height: 350px; cursor: pointer; }}
            .project-swiper .swiper-slide {{ width: 100%; height: 100%; }}
            .project-swiper .swiper-slide img {{ width: 100%; height: 100%; object-fit: cover; display: block; cursor: zoom-in; }}
            .project-swiper .swiper-button-prev, .project-swiper .swiper-button-next {{ color: white; background: rgba(15, 120, 116, 0.7); width: 40px; height: 40px; border-radius: 50%; }}
            .project-swiper .swiper-button-prev::after, .project-swiper .swiper-button-next::after {{ font-size: 18px; font-weight: bold; }}
            .project-swiper .swiper-pagination-bullet {{ background: white; opacity: 0.5; }}
            .project-swiper .swiper-pagination-bullet-active {{ background: var(--brand); opacity: 1; }}
            .project-image {{ width: 100%; height: 350px; overflow: hidden; cursor: pointer; }}
            .project-image img {{ width: 100%; height: 100%; object-fit: cover; display: block; cursor: zoom-in; }}
            .project-content {{ padding: 30px; }}
            .project-card h3 {{ margin: 0 0 15px 0; color: #222; font-size: 1.4em; }}
            .project-card p {{ font-size: 1.05em; color: #555; margin-bottom: 20px; line-height: 1.6; }}
            .stat-badge {{ display: inline-block; background: #E0F2F1; color: var(--brand); padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9em; }}
            
            .btn-group {{ text-align: center; margin-top: 50px; display: flex; justify-content: center; align-items: center; }}
            .btn-divider {{ width: 2px; height: 40px; background-color: var(--brand); margin: 0 20px; opacity: 0.5; }}
            .btn {{ padding: 16px 40px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; display: inline-block; transition: all 0.3s; }}
            .btn-primary {{ background-color: var(--brand); color: white; box-shadow: 0 4px 15px rgba(15, 120, 116, 0.3); }}
            .btn-primary:hover {{ background-color: #0a5c59; transform: scale(1.05); }}
            .btn-secondary {{ background-color: transparent; color: var(--brand); border: 2px solid var(--brand); }}
            .btn-secondary:hover {{ background-color: var(--brand); color: white; transform: scale(1.05); }}
            
            .lightbox {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.95); z-index: 9999; justify-content: center; align-items: center; cursor: zoom-out; }}
            .lightbox.active {{ display: flex; }}
            .lightbox img {{ max-width: 90%; max-height: 90%; object-fit: contain; border-radius: 8px; }}
            .lightbox-close {{ position: absolute; top: 20px; right: 40px; color: white; font-size: 40px; cursor: pointer; }}
            .lightbox-prev, .lightbox-next {{ position: absolute; top: 50%; transform: translateY(-50%); color: white; font-size: 40px; cursor: pointer; padding: 20px; }}
            .lightbox-prev {{ left: 20px; }} .lightbox-next {{ right: 20px; }}
            
            /* Стили для видео-модалки */
            .hero-clickable {{ cursor: pointer; transition: transform 0.3s; }}
            .hero-clickable:hover {{ transform: scale(1.05); }}
            .video-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.95); z-index: 10000; justify-content: center; align-items: center; }}
            .video-modal.active {{ display: flex; }}
            .video-modal-content {{ width: 90%; max-width: 1200px; position: relative; }}
            .video-modal-content video {{ width: 100%; max-height: 90vh; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }}

            .main-footer {{ background: #1a1a1a; color: #ccc; padding: 60px 20px 0; margin-top: 80px; }}
            .footer-content {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 50px; padding-bottom: 40px; border-bottom: 1px solid #333; }}
            .footer-col h3, .footer-col h4 {{ color: white; margin-top: 0; margin-bottom: 20px; }}
            .footer-logo {{ font-size: 1.8em; color: var(--brand); font-weight: bold; }}
            .footer-desc {{ font-size: 0.95em; line-height: 1.6; color: #aaa; }}
            .footer-links a, .footer-contacts a {{ display: block; color: #ccc; text-decoration: none; margin-bottom: 10px; transition: color 0.2s; }}
            .footer-links a:hover, .footer-contacts a:hover {{ color: var(--brand); }}
            .contact-item {{ display: flex; align-items: center; gap: 10px; margin-bottom: 15px; color: #ccc; font-size: 0.95em; }}
            .contact-item svg {{ color: var(--brand); flex-shrink: 0; }}
            .contact-item a {{ color: #ccc; text-decoration: none; }}
            .contact-item a:hover {{ color: var(--brand); }}
            .social-links {{ display: flex; gap: 12px; margin-top: 20px; }}
            .social-link {{ display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: #333; border-radius: 50%; color: white; transition: all 0.3s; }}
            .social-link:hover {{ background: var(--brand); transform: translateY(-3px); }}
            .footer-bottom {{ max-width: 1200px; margin: 0 auto; padding: 25px 0; text-align: center; color: #777; font-size: 0.9em; }}
            .footer-bottom p {{ margin: 0; }}

            /* === МОБИЛЬНАЯ АДАПТАЦИЯ === */
            @media (max-width: 768px) {{ 
                .main-header {{ padding: 10px 0; }}
                .main-header.scrolled {{ padding: 10px 0; }}
                .header-inner {{ flex-direction: column; gap: 10px; padding: 10px 15px; }}
                .logo-area {{ width: 100%; justify-content: center; }}
                .logo-img {{ height: 50px !important; }}
                nav {{ flex-direction: row; flex-wrap: wrap; width: 100%; gap: 5px; justify-content: center; }}
                nav a {{ font-size: 0.85em; padding: 5px 8px; text-align: center; white-space: nowrap; }}
                .language-switcher {{ margin-left: 0 !important; padding-left: 0 !important; border-left: none !important; justify-content: center; width: 100%; margin-top: 5px; gap: 5px; }}
                .lang-link {{ font-size: 0.8em; padding: 4px 8px; }}
                
                .hero {{ margin-top: 200px; height: 80vh; }}
                .hero h2 {{ font-size: 2em !important; padding: 0 15px; }}
                /* .hero-clickable::after {{ content: ' ▶'; font-size: 0.5em; opacity: 0.8; vertical-align: middle; }} */
                
                .container {{ padding: 40px 15px; margin-top: 0; }}
                h2.section-title {{ font-size: 1.6em; margin-top: 20px; }}
                .project-swiper, .project-image {{ height: 250px !important; }}
                .project-content {{ padding: 20px 15px; }}
                .project-card h3 {{ font-size: 1.2em; }}
                .btn-group {{ flex-direction: column; gap: 15px; }}
                .btn-divider {{ display: none; }}
                .btn {{ width: 100%; text-align: center; }}
                .footer-content {{ grid-template-columns: 1fr; gap: 30px; text-align: center; }}
                .social-links, .contact-item {{ justify-content: center; }}
                
                .video-modal-content {{ width: 95%; }}
            }}
            @media (max-width: 480px) {{
                .hero {{ margin-top: 100px; height: 70vh; }}
                .hero h2 {{ font-size: 1.6em !important; }}
                nav a {{ font-size: 0.75em; padding: 4px 6px; }}
                .lang-link {{ font-size: 0.7em; padding: 3px 6px; }}
                .logo-img {{ height: 45px !important; }}
            }}
        </style>
    </head>
    <body>
        <header class="main-header" id="main-header">
            <div class="header-inner">
                <div class="logo-area"><a href="/" class="logo-link"><img src="/static/logo.png" alt="Logo" class="logo-img"></a></div>
                <nav>{nav_links}{lang_switcher}</nav>
            </div>
        </header>
        
        <!-- Добавлен класс hero-clickable и onclick -->
        <div class="hero"><h2 class="hero-clickable" onclick="openHeroVideo()">{t['hero_title']}</h2></div>
        
        <div class="container" id="projects">
            <h2 class="section-title">{t['projects']}</h2>
            {projects_html}
            <h2 class="section-title" style="margin-top: 80px;">{t['how_to_help']}</h2>
            <p style="font-size: 1.2em; text-align: center; max-width: 700px; margin: 0 auto 40px;">{t['support_message']}</p>
            <div class="btn-group">
                <a href="/join/" class="btn btn-secondary">{t['join_us']}</a>
            </div>
        </div>
        
        <div class="lightbox" id="lightbox">
            <span class="lightbox-close" onclick="closeLightbox()">&times;</span>
            <span class="lightbox-prev" onclick="changeLightboxImage(-1)">&#10094;</span>
            <span class="lightbox-next" onclick="changeLightboxImage(1)">&#10095;</span>
            <img src="" alt="Full size" id="lightbox-img">
        </div>
        
<!-- Модальное окно для видео -->
<div class="video-modal" id="videoModal" onclick="closeHeroVideo(event)">
    <div class="video-modal-content">
        <video id="heroVideo" controls autoplay>
            <source src="/static/mountain-timelapse.mp4" type="video/mp4">
            Ваш браузер не поддерживает видео.
        </video>
    </div>
</div>
        
        {footer_html}
        
        <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
        <script>
            let currentLightboxIndex = 0, currentProjectImages = [];
            
            function openLightbox(imageUrl, index, projectId) {{
                const lightbox = document.getElementById('lightbox'), lightboxImg = document.getElementById('lightbox-img');
                const projectSwiper = document.getElementById(projectId);
                if (projectSwiper) {{ const images = projectSwiper.querySelectorAll('.swiper-slide img'); currentProjectImages = Array.from(images).map(img => img.src); }}
                currentLightboxIndex = index; lightboxImg.src = imageUrl; lightbox.classList.add('active'); document.body.style.overflow = 'hidden';
            }}
            function closeLightbox() {{ document.getElementById('lightbox').classList.remove('active'); document.body.style.overflow = ''; }}
            function changeLightboxImage(direction) {{
                if (currentProjectImages.length === 0) return; currentLightboxIndex += direction;
                if (currentLightboxIndex < 0) currentLightboxIndex = currentProjectImages.length - 1;
                else if (currentLightboxIndex >= currentProjectImages.length) currentLightboxIndex = 0;
                document.getElementById('lightbox-img').src = currentProjectImages[currentLightboxIndex];
            }}
            document.getElementById('lightbox').addEventListener('click', function(e) {{ if (e.target === this) closeLightbox(); }});
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') closeLightbox();
                else if (e.key === 'ArrowLeft') changeLightboxImage(-1);
                else if (e.key === 'ArrowRight') changeLightboxImage(1);
            }});
            document.addEventListener('DOMContentLoaded', function() {{
                document.querySelectorAll('.project-swiper').forEach(el => new Swiper(el, {{ loop: true, effect: 'fade', fadeEffect: {{ crossFade: true }}, speed: 800, autoplay: {{ delay: 4000 }}, navigation: {{ nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' }}, pagination: {{ el: '.swiper-pagination', clickable: true }} }}));
            }});
            window.addEventListener('scroll', function() {{
                const header = document.getElementById('main-header');
                if (window.scrollY > 50) header.classList.add('scrolled'); else header.classList.remove('scrolled');
            }});

            /* === ФУНКЦИИ ДЛЯ ВИДЕО === */
            function openHeroVideo() {{
                const modal = document.getElementById('videoModal');
                const video = document.getElementById('heroVideo');
                modal.classList.add('active');
                video.play();
                document.body.style.overflow = 'hidden';
                
                // После завершения видео — переход на /join/
                video.onended = function() {{
                    closeHeroVideo();
                    window.location.href = '/join/';
                }};
            }}

            function closeHeroVideo(event) {{
                if (event && event.target !== event.currentTarget && !event.target.classList.contains('video-modal-content')) return;
                const modal = document.getElementById('videoModal');
                const video = document.getElementById('heroVideo');
                modal.classList.remove('active');
                video.pause();
                video.currentTime = 0;
                document.body.style.overflow = '';
            }}
        </script>
    </body>
    </html>
    """
    response = HttpResponse(html)
    response.set_cookie('django_language', lang, max_age=31536000)
    return response


def join(request):
    from .forms import VolunteerForm
    from django.middleware.csrf import get_token

    lang = request.COOKIES.get('django_language', 'ru')
    if lang not in ['ru', 'en', 'hy']:
        lang = 'ru'
    activate(lang)

    t = {
        'home': _("Главная"),
        'about': _("О нас"),
        'projects': _("Проекты"),
        'join': _("Присоединяйтесь"),
        'map': _("Карта"),
        'support': _("Поддержать"),
        'join_title': _("Присоединиться"),
        'join_heading': _("Присоединяйтесь к нам!"),
        'join_description': _("Заполните форму ниже, чтобы стать частью команды Aragats Antar и принять участие в создании \"зеленого щита\" вокруг Арагаца"),
        'back_home': _("Вернуться на главную"),
        'about_project': _("О проекте"),
        'contacts': _("Контакты"),
        'submit': _("Отправить заявку"),
        'success_message': _("Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время."),
        'who_we_need': _("Кто нам нужен"),
        'join_text_1': _("<strong>Aragats Antar</strong> — это не просто проект по восстановлению лесов. Это сообщество единомышленников, где каждый может найти своё место и внести реальный вклад в сохранение климата Армении."),
        'join_text_2': _("Мы ищем <strong>агрономов и дендрологов</strong>. Нам нужны <strong>волонтёры-озеленители</strong>, готовые приехать на субботники, сажать деревья и ухаживать за саженцами."),
        'join_text_3': _("Если вы <strong>SMM-специалист</strong>, мы доверим вам ведение соцсетей и создание контента. <strong>Копирайтеры</strong> помогут нам писать тексты для сайта и СМИ. <strong>Контент-мейкеры/фотографы</strong> будут снимать видео и фотографии, показывая красоту Арагаца и процесс восстановления лесов."),
        'join_text_4': _("А если у вас есть другие таланты — дизайн, юриспруденция, бухгалтерия, логистика — мы найдём им применение!"),
        'join_text_5': _("<strong>Что вы получите?</strong> Реальный опыт, новые знакомства, уникальные фотографии на фоне гор, пополнение портфолио и осознание того, что вы делаете мир лучше. Каждое посаженное дерево — это ваш личный вклад в будущее Армении."),
    }

    nav_links = get_nav_links(t['join'], t)
    lang_switcher = get_language_switcher(lang)
    footer_html = get_footer_html(lang)
    
    form = VolunteerForm()
    success = False
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = VolunteerForm()
    
    csrf_token = get_token(request)
    html = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t['join_title']} - {BRAND_NAME}</title>
        <style>
            :root {{ --brand: {BRAND_COLOR}; }}
            html {{ scroll-behavior: smooth; }}
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #FAFAFA; color: #333; line-height: 1.6; }}
            .main-header {{ position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background-color: white; box-shadow: 0 2px 15px rgba(0,0,0,0.08); padding: 15px 0; }}
            .header-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }}
            .logo-area {{ display: flex; align-items: center; gap: 20px; }}
            .logo-link {{ text-decoration: none; display: inline-block; transition: transform 0.3s ease; }}
            .logo-link:hover {{ transform: scale(1.05); }}
            .logo-img {{ height: 70px; width: auto; }}
            nav {{ display: flex; align-items: center; gap: 20px; }}
            nav a {{ color: #333; text-decoration: none; font-weight: 600; font-size: 1.05em; transition: color 0.2s; position: relative; }}
            nav a:hover {{ color: var(--brand); }}
            nav a.active-link {{ color: var(--brand); }}
            nav a.active-link::after {{ content: ''; position: absolute; bottom: -4px; left: 0; width: 100%; height: 2px; background-color: var(--brand); }}
            .language-switcher {{ display: flex; gap: 5px; margin-left: 20px; padding-left: 20px; border-left: 1px solid rgba(0,0,0,0.1); }}
            .lang-link {{ color: #333; text-decoration: none; font-size: 0.9em; font-weight: bold; padding: 5px 8px; border-radius: 5px; transition: background 0.3s; }}
            .lang-link:hover, .lang-link.active {{ background: var(--brand); color: white !important; }}
            
            .join-intro {{ background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%); padding: 80px 20px; margin-top: 80px; }}
            .join-intro-container {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }}
            .join-intro-text {{ font-size: 1.05em; line-height: 1.8; color: #444; }}
            .join-intro-text p {{ margin-bottom: 20px; }}
            .join-intro-text strong {{ color: var(--brand); font-weight: 700; }}
            .join-intro-image {{ border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.15); transition: all 0.3s ease; }}
            .join-intro-video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
            .join-intro-title {{ font-size: 2.5em; color: var(--brand); margin-bottom: 30px; font-weight: 800; }}
            .scroll-to-form-video {{ text-decoration: none; display: block; cursor: pointer; }}
            .scroll-to-form-video:hover .join-intro-image {{ box-shadow: 0 15px 40px rgba(15, 120, 116, 0.3); transform: scale(1.02); }}
            
            .join-container {{ max-width: 700px; margin: 60px auto; padding: 0 20px; }}
            .join-header {{ text-align: center; margin-bottom: 40px; }}
            .join-header h1 {{ color: var(--brand); font-size: 2.5em; margin-bottom: 15px; }}
            .join-header p {{ font-size: 1.2em; color: #666; max-width: 600px; margin: 0 auto; line-height: 1.6; }}
            .form-wrapper {{ background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
            .form-group {{ margin-bottom: 25px; }}
            .form-group label {{ display: block; margin-bottom: 8px; font-weight: 600; color: #333; font-size: 1.05em; }}
            .form-input, .form-textarea {{ width: 100%; padding: 14px 18px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1em; transition: border-color 0.3s; box-sizing: border-box; font-family: inherit; }}
            .form-textarea {{ resize: vertical; }}
            .form-input:focus, .form-textarea:focus {{ outline: none; border-color: var(--brand); }}
            .submit-btn {{ background-color: var(--brand); color: white; padding: 16px 40px; border: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; cursor: pointer; transition: all 0.3s; width: 100%; box-shadow: 0 4px 15px rgba(15, 120, 116, 0.3); }}
            .submit-btn:hover {{ background-color: #0a5c59; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(15, 120, 116, 0.4); }}
            .success-message {{ background: #E0F2F1; color: var(--brand); padding: 20px; border-radius: 8px; text-align: center; font-size: 1.1em; margin-bottom: 30px; border-left: 4px solid var(--brand); }}
            .back-btn {{ display: inline-flex; align-items: center; margin-top: 30px; color: var(--brand); text-decoration: none; font-weight: bold; font-size: 1.1em; transition: gap 0.2s; }}
            .back-btn:hover {{ gap: 10px; }}
            .back-btn span {{ margin-right: 8px; font-size: 1.2em; }}
            
            .main-footer {{ background: #1a1a1a; color: #ccc; padding: 60px 20px 0; margin-top: 80px; }}
            .footer-content {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 50px; padding-bottom: 40px; border-bottom: 1px solid #333; }}
            .footer-col h3, .footer-col h4 {{ color: white; margin-top: 0; margin-bottom: 20px; }}
            .footer-logo {{ font-size: 1.8em; color: var(--brand); font-weight: bold; }}
            .footer-desc {{ font-size: 0.95em; line-height: 1.6; color: #aaa; }}
            .footer-links a, .footer-contacts a {{ display: block; color: #ccc; text-decoration: none; margin-bottom: 10px; transition: color 0.2s; }}
            .footer-links a:hover, .footer-contacts a:hover {{ color: var(--brand); }}
            .contact-item {{ display: flex; align-items: center; gap: 10px; margin-bottom: 15px; color: #ccc; font-size: 0.95em; }}
            .contact-item svg {{ color: var(--brand); flex-shrink: 0; }}
            .contact-item a {{ color: #ccc; text-decoration: none; }}
            .contact-item a:hover {{ color: var(--brand); }}
            .social-links {{ display: flex; gap: 12px; margin-top: 20px; }}
            .social-link {{ display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: #333; border-radius: 50%; color: white; transition: all 0.3s; }}
            .social-link:hover {{ background: var(--brand); transform: translateY(-3px); }}
            .footer-bottom {{ max-width: 1200px; margin: 0 auto; padding: 25px 0; text-align: center; color: #777; font-size: 0.9em; }}
            .footer-bottom p {{ margin: 0; }}

            /* === МОБИЛЬНАЯ АДАПТАЦИЯ === */
            @media (max-width: 768px) {{ 
                .main-header {{ padding: 10px 0; }}
                .header-inner {{ flex-direction: column; gap: 10px; padding: 10px 15px; }}
                .logo-area {{ width: 100%; justify-content: center; }}
                .logo-img {{ height: 50px !important; }}
                nav {{ flex-direction: row; flex-wrap: wrap; width: 100%; gap: 5px; justify-content: center; }}
                nav a {{ font-size: 0.85em; padding: 5px 8px; text-align: center; white-space: nowrap; }}
                .language-switcher {{ margin-left: 0 !important; padding-left: 0 !important; border-left: none !important; justify-content: center; width: 100%; margin-top: 5px; gap: 5px; }}
                .lang-link {{ font-size: 0.8em; padding: 4px 8px; }}
                
                .join-intro {{ margin-top: 200px; padding: 40px 15px; }}
                .join-intro-container {{ grid-template-columns: 1fr; }}
                .join-intro-image {{ order: -1; }}
                .join-intro-title {{ font-size: 1.8em; }}
                .join-container {{ padding: 0 15px; margin: 40px auto; }}
                .join-header h1 {{ font-size: 1.8em; }}
                .form-wrapper {{ padding: 25px 20px; }}
                .footer-content {{ grid-template-columns: 1fr; gap: 30px; text-align: center; }}
                .social-links, .contact-item {{ justify-content: center; }}
            }}
        </style>
    </head>
    <body>
        <header class="main-header">
            <div class="header-inner">
                <div class="logo-area"><a href="/" class="logo-link"><img src="/static/logo.png" alt="Logo" class="logo-img"></a></div>
                <nav>{nav_links}{lang_switcher}</nav>
            </div>
        </header>
        
        <div class="join-intro">
            <div class="join-intro-container">
                <div class="join-intro-text">
                    <h2 class="join-intro-title">{t['who_we_need']}</h2>
                    <p>{t['join_text_1']}</p>
                    <p>{t['join_text_2']}</p>
                    <p>{t['join_text_3']}</p>
                    <p>{t['join_text_4']}</p>
                    <p>{t['join_text_5']}</p>
                </div>
                <a href="#join-form" class="scroll-to-form-video">
                    <div class="join-intro-image">
                        <video autoplay muted playsinline class="join-intro-video">
                            <source src="/static/join-video.mp4" type="video/mp4">
                            Ваш браузер не поддерживает видео.
                        </video>
                    </div>
                </a>
            </div>
        </div>
        
        <div class="join-container" id="join-form">
            <div class="join-header"><h1>{t['join_heading']}</h1><p>{t['join_description']}</p></div>
            <div class="form-wrapper">
                {'<div class="success-message">' + t['success_message'] + '</div>' if success else ''}
                <form method="post" action="">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <div class="form-group"><label for="id_name">{_('Ваше имя')}</label><input type="text" name="name" id="id_name" class="form-input" required></div>
                    <div class="form-group"><label for="id_email">Email</label><input type="email" name="email" id="id_email" class="form-input" required></div>
                    <div class="form-group"><label for="id_phone">{_('Телефон')}</label><input type="text" name="phone" id="id_phone" class="form-input"></div>
                    <div class="form-group"><label for="id_message">{_('Сообщение')}</label><textarea name="message" id="id_message" class="form-textarea" rows="5"></textarea></div>
                    <button type="submit" class="submit-btn">{t['submit']}</button>
                </form>
            </div>
            <div style="text-align: center;"><a href="/" class="back-btn"><span>←</span> {t['back_home']}</a></div>
        </div>
        {footer_html}
    </body>
    </html>
    """
    response = HttpResponse(html)
    response.set_cookie('django_language', lang, max_age=31536000)
    return response


def about(request):
    lang = request.COOKIES.get('django_language', 'ru')
    if lang not in ['ru', 'en', 'hy']:
        lang = 'ru'
    activate(lang)
    
    page = AboutPage.objects.first()
    t = {
        'home': _("Главная"), 
        'about': _("О нас"), 
        'projects': _("Проекты"), 
        'map': _("Карта"),
        'join': _("Присоединяйтесь"),
        'support': _("Поддержать"),
        'back_home': _("Вернуться на главную"), 
        'about_filling': _("Раздел 'О нас' пока заполняется... Мы добавляем историю нашей организации."),
    }

    nav_links = get_nav_links(t['about'], t)
    lang_switcher = get_language_switcher(lang)
    footer_html = get_footer_html(lang)
    
    if not page:
        text = f"<p>{t['about_filling']}</p>"
        image_html = ""
        page_title = t['about']
    else:
        page_title = page.title if page.title else t['about']
        
        if page.content:
            paragraphs = str(page.content).split('\n\n')
            text = "".join([f"<p>{p.strip()}</p>" for p in paragraphs if p.strip()])
        else:
            text = f"<p>{t['about_filling']}</p>"
            
        image_html = ""
        if page.image:
            try:
                image_html = f'<div class="about-image"><img src="{page.image.url}" alt="{page_title}"></div>'
            except ValueError:
                image_html = ""
        
    html = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{page_title} - {BRAND_NAME}</title>
        <style>
            :root {{ --brand: {BRAND_COLOR}; }}
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #FAFAFA; color: #333; line-height: 1.7; }}
            .main-header {{ position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background-color: white; box-shadow: 0 2px 15px rgba(0,0,0,0.08); padding: 15px 0; }}
            .header-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }}
            .logo-area {{ display: flex; align-items: center; gap: 20px; }}
            .logo-link {{ text-decoration: none; display: inline-block; transition: transform 0.3s ease; }}
            .logo-link:hover {{ transform: scale(1.05); }}
            .logo-img {{ height: 70px; width: auto; filter: none; }}
            nav {{ display: flex; align-items: center; gap: 20px; }}
            nav a {{ color: #333; text-decoration: none; font-weight: 600; font-size: 1.05em; transition: color 0.2s; position: relative; }}
            nav a:hover {{ color: var(--brand); }}
            nav a.active-link {{ color: var(--brand); }}
            nav a.active-link::after {{ content: ''; position: absolute; bottom: -4px; left: 0; width: 100%; height: 2px; background-color: var(--brand); }}
            .language-switcher {{ display: flex; gap: 5px; margin-left: 20px; padding-left: 20px; border-left: 1px solid rgba(0,0,0,0.1); }}
            .lang-link {{ color: #333; text-decoration: none; font-size: 0.9em; font-weight: bold; padding: 5px 8px; border-radius: 5px; transition: background 0.3s; }}
            .lang-link:hover, .lang-link.active {{ background: var(--brand); color: white !important; }}
            .about-container {{ max-width: 900px; margin: 120px auto 60px; padding: 0 20px; background: white; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
            h1.page-title {{ color: var(--brand); font-size: 2.5em; margin-top: 0; margin-bottom: 40px; border-bottom: 2px solid #eee; padding-bottom: 20px; }}
            .about-image {{ margin: 40px 0; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.15); }}
            .about-image img {{ width: 100%; height: auto; display: block; }}
            .story-content p {{ font-size: 1.15em; margin-bottom: 25px; color: #444; text-align: justify; }}
            .back-btn {{ display: inline-flex; align-items: center; margin-top: 50px; color: var(--brand); text-decoration: none; font-weight: bold; font-size: 1.1em; transition: gap 0.2s; }}
            .back-btn:hover {{ gap: 10px; }} .back-btn span {{ margin-right: 8px; font-size: 1.2em; }}
            .main-footer {{ background: #1a1a1a; color: #ccc; padding: 60px 20px 0; margin-top: 80px; }}
            .footer-content {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 50px; padding-bottom: 40px; border-bottom: 1px solid #333; }}
            .footer-col h3, .footer-col h4 {{ color: white; margin-top: 0; margin-bottom: 20px; }}
            .footer-logo {{ font-size: 1.8em; color: var(--brand); font-weight: bold; }}
            .footer-desc {{ font-size: 0.95em; line-height: 1.6; color: #aaa; }}
            .footer-links a, .footer-contacts a {{ display: block; color: #ccc; text-decoration: none; margin-bottom: 10px; transition: color 0.2s; }}
            .footer-links a:hover, .footer-contacts a:hover {{ color: var(--brand); }}
            .contact-item {{ display: flex; align-items: center; gap: 10px; margin-bottom: 15px; color: #ccc; font-size: 0.95em; }}
            .contact-item svg {{ color: var(--brand); flex-shrink: 0; }}
            .contact-item a {{ color: #ccc; text-decoration: none; }}
            .contact-item a:hover {{ color: var(--brand); }}
            .social-links {{ display: flex; gap: 12px; margin-top: 20px; }}
            .social-link {{ display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: #333; border-radius: 50%; color: white; transition: all 0.3s; }}
            .social-link:hover {{ background: var(--brand); transform: translateY(-3px); }}
            .footer-bottom {{ max-width: 1200px; margin: 0 auto; padding: 25px 0; text-align: center; color: #777; font-size: 0.9em; }}
            .footer-bottom p {{ margin: 0; }}

            /* === МОБИЛЬНАЯ АДАПТАЦИЯ === */
            @media (max-width: 768px) {{ 
                .main-header {{ padding: 10px 0; }}
                .header-inner {{ flex-direction: column; gap: 10px; padding: 10px 15px; }}
                .logo-area {{ width: 100%; justify-content: center; }}
                .logo-img {{ height: 50px !important; }}
                nav {{ flex-direction: row; flex-wrap: wrap; width: 100%; gap: 5px; justify-content: center; }}
                nav a {{ font-size: 0.85em; padding: 5px 8px; text-align: center; white-space: nowrap; }}
                .language-switcher {{ margin-left: 0 !important; padding-left: 0 !important; border-left: none !important; justify-content: center; width: 100%; margin-top: 5px; gap: 5px; }}
                .lang-link {{ font-size: 0.8em; padding: 4px 8px; }}
                
                .about-container {{ margin: 200px 15px 40px; padding: 20px; }}
                h1.page-title {{ font-size: 1.8em; }}
                .story-content p {{ font-size: 1em; text-align: left; }}
                .footer-content {{ grid-template-columns: 1fr; gap: 30px; text-align: center; }}
                .social-links, .contact-item {{ justify-content: center; }}
            }}
        </style>
    </head>
    <body>
        <header class="main-header">
            <div class="header-inner">
                <div class="logo-area"><a href="/" class="logo-link"><img src="/static/logo.png" alt="Logo" class="logo-img"></a></div>
                <nav>{nav_links}{lang_switcher}</nav>
            </div>
        </header>
        <div class="about-container">
            <h1 class="page-title">{page_title}</h1>
            {image_html}
            <div class="story-content">{text}</div>
            <a href="/" class="back-btn"><span>←</span> {t['back_home']}</a>
        </div>
        {footer_html}
    </body>
    </html>
    """
    response = HttpResponse(html)
    response.set_cookie('django_language', lang, max_age=31536000)
    return response


def support(request):
    lang = request.COOKIES.get('django_language', 'ru')
    if lang not in ['ru', 'en', 'hy']:
        lang = 'ru'
    activate(lang)

    # =========================================================
    # НАСТРОЙКА ДОНАТОВ (ЗАПОЛНИТЕ ЭТИ ДАННЫЕ!)
    # =========================================================
    QR_USDT = "/static/qr_usdt.png"
    QR_TON = "/static/qr_ton.png"
    QR_BTC = "/static/qr_btc.png"
    QR_ETH = "/static/qr_eth.png"
    
    ICON_USDT = "https://cryptologos.cc/logos/tether-usdt-logo.png"
    ICON_TON = "https://cryptologos.cc/logos/toncoin-ton-logo.png"
    ICON_BTC = "https://cryptologos.cc/logos/bitcoin-btc-logo.png"
    ICON_ETH = "https://cryptologos.cc/logos/ethereum-eth-logo.png"
    
    ADDR_USDT = "TUhwBwMRKiWwsg9YvXCe5bTEgdpRj366Qg"
    ADDR_TON = "UQCzOa29c8ycE6FP4Pf7nZ3vAX5cnyXt9lnmjcgttiG-ApoO"
    ADDR_BTC = "bc1q85dfm6g2stmpesrzcn5mrvq8fhm20t28qau60d"
    ADDR_ETH = "0x70C70e9D3a30E50A4075Dbc7575b5A5C6015b67a"
    
    BANK_CARD_NUMBER = "4374 7201 0002 2469"
    BANK_CARD_HOLDER = "ARAGATS ANTAR CHARITAB.NGO"
    # =========================================================

    t = {
        'home': _("Главная"),
        'about': _("О нас"),
        'projects': _("Проекты"),
        'map': _("Карта"),
        'join': _("Присоединяйтесь"),
        'support': _("Поддержать"),
        'support_title': _("Поддержите восстановление лесов Армении"),
        'support_subtitle': _("Выберите удобный способ пожертвования. Все переводы безопасны и идут напрямую на посадку деревьев."),
        'copy_address': _("Копировать адрес"),
        'copied': _("Скопировано!"),
        'scan_qr': _("Отсканируйте QR-код"),
        'bank_transfer': _("Банковский перевод"),
        'bank_transfer_desc': _("Прямой перевод на карту или расчетный счет"),
        'crypto_title': _("Криптовалюта"),
        'crypto_desc': _("Мгновенные переводы без посредников"),
        'corporate_title': _("Корпоративным партнерам"),
        'corporate_desc': _("Для крупных пожертвований используйте банковский перевод по реквизитам."),
        'bank_name': _("Банк получателя"),
        'account_name': _("Получатель"),
        'contact_for_corp': _("Связаться для партнерства"),
        # Названия криптовалют
        'usdt_name': _("USDT (TRC20)"),
        'usdt_desc': _("Рекомендуем: низкие комиссии"),
        'ton_name': _("TON"),
        'ton_desc': _("Удобно из Telegram"),
        'btc_name': _("Bitcoin (BTC)"),
        'btc_desc': _("Классика, надежно"),
        'eth_name': _("Ethereum (ETH)"),
        'eth_desc': _("Популярная сеть"),
    }

    nav_links = get_nav_links(t['support'], t)
    lang_switcher = get_language_switcher(lang)
    footer_html = get_footer_html(lang)

    crypto_methods = [
        {
            'name': t['usdt_name'],
            'desc': t['usdt_desc'],
            'icon': ICON_USDT,
            'qr': QR_USDT,
            'address': ADDR_USDT,
            'color': '#26a17b'
        },
        {
            'name': t['ton_name'],
            'desc': t['ton_desc'],
            'icon': ICON_TON,
            'qr': QR_TON,
            'address': ADDR_TON,
            'color': '#0088cc'
        },
        {
            'name': t['btc_name'],
            'desc': t['btc_desc'],
            'icon': ICON_BTC,
            'qr': QR_BTC,
            'address': ADDR_BTC,
            'color': '#f7931a'
        },
        {
            'name': t['eth_name'],
            'desc': t['eth_desc'],
            'icon': ICON_ETH,
            'qr': QR_ETH,
            'address': ADDR_ETH,
            'color': '#627eea'
        }
    ]

    crypto_cards_html = ""
    for crypto in crypto_methods:
        crypto_cards_html += f"""
        <div class="payment-card crypto-card">
            <div class="crypto-header">
                <img src="{crypto['icon']}" alt="{crypto['name']}" class="crypto-icon-img">
                <div>
                    <h3>{crypto['name']}</h3>
                    <p>{crypto['desc']}</p>
                </div>
            </div>
            <div class="qr-container">
                <img src="{crypto['qr']}" alt="QR {crypto['name']}" class="qr-image">
                <span class="qr-hint">{t['scan_qr']}</span>
            </div>
            <div class="address-box">
                <code id="addr-{crypto['name'].replace(' ', '')}">{crypto['address']}</code>
                <button class="copy-btn" onclick="copyToClipboard('addr-{crypto['name'].replace(' ', '')}', this)">
                    📋 {t['copy_address']}
                </button>
            </div>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t['support']} - {BRAND_NAME}</title>
        <style>
            :root {{ --brand: {BRAND_COLOR}; }}
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #FAFAFA; color: #333; line-height: 1.6; }}
            .main-header {{ position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background-color: white; box-shadow: 0 2px 15px rgba(0,0,0,0.08); padding: 15px 0; }}
            .header-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }}
            .logo-area {{ display: flex; align-items: center; gap: 20px; }}
            .logo-link {{ text-decoration: none; display: inline-block; }}
            .logo-img {{ height: 70px; width: auto; }}
            nav {{ display: flex; align-items: center; gap: 20px; }}
            nav a {{ color: #333; text-decoration: none; font-weight: 600; font-size: 1.05em; transition: color 0.2s; position: relative; }}
            nav a:hover, nav a.active-link {{ color: var(--brand); }}
            nav a.active-link::after {{ content: ''; position: absolute; bottom: -4px; left: 0; width: 100%; height: 2px; background-color: var(--brand); }}
            .language-switcher {{ display: flex; gap: 5px; margin-left: 20px; padding-left: 20px; border-left: 1px solid rgba(0,0,0,0.1); }}
            .lang-link {{ color: #333; text-decoration: none; font-size: 0.9em; font-weight: bold; padding: 5px 8px; border-radius: 5px; transition: background 0.3s; }}
            .lang-link:hover, .lang-link.active {{ background: var(--brand); color: white !important; }}

            .support-hero {{
                background: linear-gradient(135deg, rgba(15, 120, 116, 0.9), rgba(15, 120, 116, 0.7)), url('/static/hero.jpg');
                background-size: cover; background-position: center;
                color: white; text-align: center; padding: 120px 20px 60px;
            }}
            .support-hero h1 {{ font-size: 2.8em; margin: 0 0 15px; font-weight: 800; }}
            .support-hero p {{ font-size: 1.2em; max-width: 700px; margin: 0 auto; opacity: 0.9; }}

            .support-container {{ max-width: 1100px; margin: -40px auto 60px; padding: 0 20px; position: relative; z-index: 10; }}
            
            .section-title {{ text-align: center; color: var(--brand); font-size: 1.8em; margin: 40px 0 25px; font-weight: 700; }}
            
            .payment-methods {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px;
                margin-bottom: 60px;
            }}
            
            .payment-card {{
                background: white;
                border-radius: 16px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.08);
                border: 2px solid transparent;
                transition: all 0.3s ease;
            }}
            .payment-card:hover {{ border-color: var(--brand); transform: translateY(-5px); }}
            
            .bank-card-highlight {{
                grid-column: 1 / -1;
                background: linear-gradient(135deg, var(--brand) 0%, #0a5c59 100%);
                color: white;
                text-align: center;
            }}
            .bank-card-highlight h3 {{ color: white; font-size: 1.5em; }}
            .bank-card-highlight p {{ color: rgba(255,255,255,0.9); }}
            .bank-number {{ 
                font-family: 'Courier New', monospace; font-size: 2em; font-weight: bold; 
                letter-spacing: 2px; background: rgba(255,255,255,0.15); padding: 20px; 
                border-radius: 12px; margin: 20px 0; word-break: break-all;
            }}
            .bank-holder {{ font-size: 1.1em; opacity: 0.9; margin-bottom: 20px; }}
            
            .crypto-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 20px; }}
            .crypto-icon-img {{ width: 50px; height: 50px; object-fit: contain; }}
            .crypto-header h3 {{ margin: 0; font-size: 1.3em; color: #333; }}
            .crypto-header p {{ margin: 5px 0 0; color: #666; font-size: 0.9em; }}
            
            .qr-container {{ text-align: center; margin: 20px 0; }}
            .qr-image {{ width: 180px; height: 180px; border: 3px solid var(--brand); border-radius: 12px; padding: 10px; background: white; }}
            .qr-hint {{ display: block; margin-top: 10px; color: #888; font-size: 0.9em; }}
            
            .address-box {{ 
                display: flex; gap: 10px; background: #F4F8F8; border: 1px solid #E0F2F1; 
                border-radius: 8px; padding: 12px; align-items: center;
            }}
            .address-box code {{ 
                flex: 1; font-family: 'Courier New', monospace; font-size: 0.85em; 
                color: #333; word-break: break-all; background: transparent; border: none;
            }}
            .copy-btn {{
                background: var(--brand); color: white; border: none; padding: 10px 15px;
                border-radius: 6px; cursor: pointer; font-size: 0.9em; font-weight: 600;
                transition: background 0.3s; white-space: nowrap;
            }}
            .copy-btn:hover {{ background: #0a5c59; }}
            .copy-btn.copied {{ background: #28a745; }}
            
            .corporate-section {{
                background: white; border-radius: 16px; padding: 40px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.05); border-left: 5px solid var(--brand);
            }}
            .corporate-section h2 {{ color: var(--brand); margin-top: 0; }}
            .bank-details {{
                background: #F4F8F8; padding: 25px; border-radius: 8px; margin: 20px 0;
                font-family: 'Courier New', monospace; font-size: 0.95em; color: #333;
            }}
            .bank-details div {{ margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #ddd; }}
            .bank-details div:last-child {{ border-bottom: none; margin-bottom: 0; }}
            .bank-details strong {{ color: var(--brand); display: inline-block; min-width: 150px; }}
            
            .btn-primary {{
                display: inline-block; background-color: var(--brand); color: white;
                padding: 14px 30px; border-radius: 8px; text-decoration: none; font-weight: bold;
                margin-top: 20px; transition: all 0.3s;
            }}
            .btn-primary:hover {{ background-color: #0a5c59; transform: translateY(-2px); }}
            
            .main-footer {{ background: #1a1a1a; color: #ccc; padding: 60px 20px 0; margin-top: 80px; }}
            .footer-content {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 50px; padding-bottom: 40px; border-bottom: 1px solid #333; }}
            .footer-col h3, .footer-col h4 {{ color: white; margin-top: 0; margin-bottom: 20px; }}
            .footer-logo {{ font-size: 1.8em; color: var(--brand); font-weight: bold; }}
            .footer-desc {{ font-size: 0.95em; line-height: 1.6; color: #aaa; }}
            .footer-links a, .footer-contacts a {{ display: block; color: #ccc; text-decoration: none; margin-bottom: 10px; transition: color 0.2s; }}
            .footer-links a:hover, .footer-contacts a:hover {{ color: var(--brand); }}
            .contact-item {{ display: flex; align-items: center; gap: 10px; margin-bottom: 15px; color: #ccc; font-size: 0.95em; }}
            .contact-item svg {{ color: var(--brand); flex-shrink: 0; }}
            .contact-item a {{ color: #ccc; text-decoration: none; }}
            .social-links {{ display: flex; gap: 12px; margin-top: 20px; }}
            .social-link {{ display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: #333; border-radius: 50%; color: white; transition: all 0.3s; }}
            .social-link:hover {{ background: var(--brand); transform: translateY(-3px); }}
            .footer-bottom {{ max-width: 1200px; margin: 0 auto; padding: 25px 0; text-align: center; color: #777; font-size: 0.9em; }}

            @media (max-width: 768px) {{
                .main-header {{ padding: 10px 0; }}
                .header-inner {{ flex-direction: column; gap: 10px; padding: 10px 15px; }}
                .logo-area {{ width: 100%; justify-content: center; }}
                .logo-img {{ height: 50px !important; }}
                nav {{ flex-direction: row; flex-wrap: wrap; width: 100%; gap: 5px; justify-content: center; }}
                nav a {{ font-size: 0.85em; padding: 5px 8px; text-align: center; white-space: nowrap; }}
                .language-switcher {{ margin-left: 0 !important; padding-left: 0 !important; border-left: none !important; justify-content: center; width: 100%; margin-top: 5px; gap: 5px; }}
                .lang-link {{ font-size: 0.8em; padding: 4px 8px; }}
                .support-hero {{ padding: 200px 15px 40px; }}
                .support-hero h1 {{ font-size: 1.8em !important; }}
                .support-container {{ padding: 0 15px; margin-top: -20px; }}
                .payment-methods {{ grid-template-columns: 1fr; }}
                .bank-number {{ font-size: 1.2em; letter-spacing: 1px; }}
                .address-box {{ flex-direction: column; align-items: stretch; }}
                .copy-btn {{ width: 100%; text-align: center; }}
                .corporate-section {{ padding: 25px 20px; }}
                .bank-details strong {{ display: block; min-width: auto; margin-bottom: 5px; }}
                .footer-content {{ grid-template-columns: 1fr; gap: 30px; text-align: center; }}
                .social-links, .contact-item {{ justify-content: center; }}
            }}
        </style>
    </head>
    <body>
        <header class="main-header">
            <div class="header-inner">
                <div class="logo-area"><a href="/" class="logo-link"><img src="/static/logo.png" alt="Logo" class="logo-img"></a></div>
                <nav>{nav_links}{lang_switcher}</nav>
            </div>
        </header>

        <div class="support-hero">
            <h1>{t['support_title']}</h1>
            <p>{t['support_subtitle']}</p>
        </div>

        <div class="support-container">
            <h2 class="section-title">{t['bank_transfer']}</h2>
            <div class="payment-methods">
                <div class="payment-card bank-card-highlight">
                    <h3>💳 {t['bank_transfer']}</h3>
                    <p>{t['bank_transfer_desc']}</p>
                    <div class="bank-number" id="bankCard">{BANK_CARD_NUMBER}</div>
                    <div class="bank-holder">{BANK_CARD_HOLDER}</div>
                    <button class="copy-btn" style="background: white; color: var(--brand);" onclick="copyToClipboard('bankCard', this)">
                         {t['copy_address']}
                    </button>
                </div>
            </div>

            <h2 class="section-title">{t['crypto_title']}</h2>
            <div class="payment-methods">
                {crypto_cards_html}
            </div>

            <div class="corporate-section">
                <h2>{t['corporate_title']}</h2>
                <p>{t['corporate_desc']}</p>
                <div class="bank-details">
                    <div><strong>{t['bank_name']}:</strong> UNIBANK O.J.S.C</div>
                    <div><strong>SWIFT:</strong> UNIJAM22XXX</div>
                    <div><strong>{t['account_name']}:</strong> ARAGATS ANTAR Charitable NGO </div>
                    <div><strong>Account (USD):</strong> 24125016452202 <em style="color: #999;">(замените на реальный)
                    <div><strong>Account (AMD):</strong> 24125016452200 </div>
                    <div><strong>Account (RUB):</strong> 24125016452201</div>
</em></div>
                </div>
                <a href="mailto:info@aragatsantar.am?subject=Корпоративное партнерство" class="btn-primary">{t['contact_for_corp']}</a>
            </div>
        </div>

        {footer_html}
        
        <script>
            function copyToClipboard(elementId, btnElement) {{
                const text = document.getElementById(elementId).innerText.replace(/\\s+/g, ' ').trim();
                navigator.clipboard.writeText(text).then(() => {{
                    const originalText = btnElement.innerHTML;
                    btnElement.innerHTML = '✅ {t['copied']}';
                    btnElement.classList.add('copied');
                    setTimeout(() => {{
                        btnElement.innerHTML = originalText;
                        btnElement.classList.remove('copied');
                    }}, 2000);
                }}).catch(err => {{
                    const textArea = document.createElement("textarea");
                    textArea.value = text;
                    document.body.appendChild(textArea);
                    textArea.select();
                    document.execCommand("copy");
                    document.body.removeChild(textArea);
                    alert("{t['copied']}");
                }});
            }}
        </script>
    </body>
    </html>
    """
    response = HttpResponse(html)
    response.set_cookie('django_language', lang, max_age=31536000)
    return response
# =========================================================
# ВРЕМЕННАЯ ФУНКЦИЯ ДЛЯ ИМПОРТА ДАННЫХ (УДАЛИТЬ ПОСЛЕ ИСПОЛЬЗОВАНИЯ)
# =========================================================
from django.core.management import call_command

def import_data(request):
    try:
        call_command('loaddata', 'fixtures.json')
        return HttpResponse("""
            <h1 style="color: green; text-align: center; margin-top: 50px;">✅ Данные успешно импортированы!</h1>
            <p style="text-align: center;">Проекты, тексты и контакты перенесены на сервер.</p>
            <p style="text-align: center;">
                <a href="/" style="color: blue; margin: 10px;">Перейти на главную</a> | 
                <a href="/admin/" style="color: blue; margin: 10px;">В админку</a>
            </p>
            <p style="color: red; text-align: center; margin-top: 50px; font-weight: bold;">
                ️ ВАЖНО: Удалите функцию import_data из views.py и маршрут из urls.py после использования!
            </p>
        """)
    except Exception as e:
        return HttpResponse(f"<h1 style='color: red;'> Ошибка импорта:</h1><p>{str(e)}</p><p>Проверьте, что файл fixtures.json существует в корне проекта.</p>")


from django.contrib.auth.models import User

def make_admin_now(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@a.am', 'admin12345')
        return HttpResponse("<h1 style='color:green; text-align:center; margin-top:50px;'>✅ АДМИН СОЗДАН! Логин: admin, Пароль: admin12345</h1><p style='text-align:center;'><a href='/admin/'>Войти в админку</a></p>")
    return HttpResponse("<h1>Админ уже существует. <a href='/admin/'>Войти</a></h1>")

def map_page(request):
    lang = request.COOKIES.get('django_language', 'ru')
    if lang not in ['ru', 'en', 'hy']:
        lang = 'ru'
    activate(lang)

    t = {
        'home': _("Главная"),
        'about': _("О нас"),
        'projects': _("Проекты"),
        'join': _("Присоединяйтесь"),
        'map': _("Карта"),
        'map_title': _("Карта озеленения"),
        'back_home': _("Вернуться на главную"),
    }

    nav_links = get_nav_links(t['map'], t)
    lang_switcher = get_language_switcher(lang)
    footer_html = get_footer_html(lang)

    import json
    import math
    
    stages = [
        {
            'name': "1-й этап",
            'year': 2023,
            'trees': 4690,
            'description': "Уже посаженный участок леса",
            'status': 'planted',
            'polygons': [
                [
                    [40.60851566889554, 43.95913580526462],
                    [40.60851566889554, 43.95913580526462],
                    [40.60850190471825, 43.95917428776418],
                    [40.6074388, 43.9586374],
                    [40.6075567, 43.9582244],
                    [40.6075301, 43.9576642],
                    [40.6077029, 43.956859],
                    [40.608456, 43.9571391],
                    [40.6086825, 43.9572659],
                    [40.6087591, 43.9574971],
                    [40.6094534, 43.9576214],
                    [40.6088197, 43.9583672],
                    [40.60851566889554, 43.95913580526462]
                ]
            ]
        },
        {
            'name': "2-й этап",
            'year': 2024,
            'trees': 0,
            'description': "Второй этап озеленения",
            'status': 'planned',
            'polygons': [
                [
                    [40.60851566889554, 43.95913580526462],
                    [40.60851566889554, 43.95913580526462],
                    [40.60850190471825, 43.95917428776418],
                    [40.6074388, 43.9586374],
                    [40.6075567, 43.9582244],
                    [40.6075301, 43.9576642],
                    [40.6077029, 43.956859],
                    [40.608456, 43.9571391],
                    [40.6086825, 43.9572659],
                    [40.6087591, 43.9574971],
                    [40.6094534, 43.9576214],
                    [40.6088197, 43.9583672],
                    [40.60851566889554, 43.95913580526462]
                ],
                [
                    [40.60744650324921, 43.958700165936285],
                    [40.60744650324921, 43.958700165936285],
                    [40.6084657, 43.9592305],
                    [40.6080714, 43.9603704],
                    [40.6079294, 43.9602043],
                    [40.6076935, 43.9606951],
                    [40.6072564, 43.960346],
                    [40.6067027, 43.9614683],
                    [40.6062853, 43.9626769],
                    [40.6061554, 43.9625989],
                    [40.6061197, 43.9625416],
                    [40.6064874, 43.9611672],
                    [40.606848, 43.9600605],
                    [40.60744650324921, 43.958700165936285]
                ]
            ]
        },
        {
            'name': "3-й этап",
            'year': 2025,
            'trees': 0,
            'description': "Третий этап озеленения",
            'status': 'planned',
            'polygons': [
                [
                    [40.60851566889554, 43.95913580526462],
                    [40.60851566889554, 43.95913580526462],
                    [40.60850190471825, 43.95917428776418],
                    [40.6074388, 43.9586374],
                    [40.6075567, 43.9582244],
                    [40.6075301, 43.9576642],
                    [40.6077029, 43.956859],
                    [40.608456, 43.9571391],
                    [40.6086825, 43.9572659],
                    [40.6087591, 43.9574971],
                    [40.6094534, 43.9576214],
                    [40.6088197, 43.9583672],
                    [40.60851566889554, 43.95913580526462]
                ],
                [
                    [40.60744650324921, 43.958700165936285],
                    [40.60744650324921, 43.958700165936285],
                    [40.6084657, 43.9592305],
                    [40.6080714, 43.9603704],
                    [40.6079294, 43.9602043],
                    [40.6076935, 43.9606951],
                    [40.6072564, 43.960346],
                    [40.6067027, 43.9614683],
                    [40.6062853, 43.9626769],
                    [40.6061554, 43.9625989],
                    [40.6061197, 43.9625416],
                    [40.6064874, 43.9611672],
                    [40.606848, 43.9600605],
                    [40.60744650324921, 43.958700165936285]
                ],
                [
                    [40.6073058, 43.9586939],
                    [40.6073058, 43.9586939],
                    [40.6070393, 43.95848],
                    [40.6054053, 43.9625384],
                    [40.6045736, 43.9623741],
                    [40.603672, 43.9637843],
                    [40.6014827, 43.9674133],
                    [40.6024745, 43.9687942],
                    [40.6029645, 43.969303],
                    [40.6045882, 43.9656928],
                    [40.6073058, 43.9586939]
                ]
            ]
        }
    ]

    # Рассчитываем площадь каждого этапа в гектарах
    def calculate_area_hectares(polygon_coords):
        """Рассчитывает площадь полигона в гектарах"""
        n = len(polygon_coords)
        if n < 3:
            return 0
        
        # Среднее значение широты для расчета
        avg_lat = sum(coord[0] for coord in polygon_coords) / n
        
        # Конвертация градусов в метры
        lat_to_m = 111320  # 1 градус широты ≈ 111.32 км
        lon_to_m = 111320 * math.cos(math.radians(avg_lat))  # 1 градус долготы зависит от широты
        
        # Формула Shoelace (Гаусса) для площади
        area_m2 = 0
        for i in range(n):
            j = (i + 1) % n
            area_m2 += polygon_coords[i][1] * lon_to_m * polygon_coords[j][0] * lat_to_m
            area_m2 -= polygon_coords[j][1] * lon_to_m * polygon_coords[i][0] * lat_to_m
        
        area_m2 = abs(area_m2) / 2
        area_hectares = area_m2 / 10000  # 1 гектар = 10000 м²
        
        return round(area_hectares, 2)

    # Добавляем информацию о гектарах для каждого этапа
    for stage in stages:
        total_area = sum(calculate_area_hectares(polygon) for polygon in stage['polygons'])
        stage['hectares'] = total_area
        # Рассчитываем количество деревьев из расчета 4500 деревьев на гектар
        if stage['status'] == 'planted':
            stage['trees'] = int(total_area * 4500)

    stages_json_str = json.dumps(stages, ensure_ascii=False)

    html = f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{t['map_title']} - {BRAND_NAME}</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <style>
            :root {{ --brand: {BRAND_COLOR}; }}
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #FAFAFA; color: #333; line-height: 1.6; }}
            .main-header {{ position: fixed; top: 0; left: 0; width: 100%; z-index: 1000; background-color: white; box-shadow: 0 2px 15px rgba(0,0,0,0.08); padding: 15px 0; }}
            .header-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }}
            .logo-area {{ display: flex; align-items: center; gap: 20px; }}
            .logo-link {{ text-decoration: none; display: inline-block; }}
            .logo-img {{ height: 70px; width: auto; }}
            nav {{ display: flex; align-items: center; gap: 20px; }}
            nav a {{ color: #333; text-decoration: none; font-weight: 600; font-size: 1.05em; transition: color 0.2s; position: relative; }}
            nav a:hover, nav a.active-link {{ color: var(--brand); }}
            nav a.active-link::after {{ content: ''; position: absolute; bottom: -4px; left: 0; width: 100%; height: 2px; background-color: var(--brand); }}
            .language-switcher {{ display: flex; gap: 5px; margin-left: 20px; padding-left: 20px; border-left: 1px solid rgba(0,0,0,0.1); }}
            .lang-link {{ color: #333; text-decoration: none; font-size: 0.9em; font-weight: bold; padding: 5px 8px; border-radius: 5px; transition: background 0.3s; }}
            .lang-link:hover, .lang-link.active {{ background: var(--brand); color: white !important; }}

            .map-hero {{
                background: linear-gradient(135deg, rgba(15, 120, 116, 0.9), rgba(15, 120, 116, 0.7)), url('/static/hero.jpg');
                background-size: cover; background-position: center;
                color: white; text-align: center; padding: 80px 20px 40px;
            }}
            .map-hero h1 {{ font-size: 2.5em; margin: 0 0 15px; font-weight: 800; }}

            .map-container {{ max-width: 1200px; margin: -40px auto 60px; padding: 0 20px; position: relative; z-index: 10; }}
            .map-wrapper {{
                background: white;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            #map {{ height: 600px; width: 100%; }}

            .legend {{
                background: white;
                padding: 20px;
                border-radius: 12px;
                margin-top: 30px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            }}
            .legend h3 {{ color: var(--brand); margin-top: 0; }}
            .legend-item {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }}
            .legend-color {{ width: 30px; height: 20px; border-radius: 4px; opacity: 0.7; }}
            .legend-color.stage1 {{ background: #2ecc71; border: 2px solid #27ae60; }}
            .legend-color.stage2 {{ background: #f39c12; border: 2px solid #e67e22; }}
            .legend-color.stage3 {{ background: #e74c3c; border: 2px solid #c0392b; }}

            .stats {{
                display: grid;
                grid-template-columns: 1fr;
                max-width: 400px;
                margin: 30px auto;
            }}
            .stat-card {{
                background: white;
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            }}
            .stat-number {{ font-size: 2.5em; font-weight: 800; color: var(--brand); }}
            .stat-label {{ color: #666; font-size: 0.95em; margin-top: 5px; }}

            .back-btn {{ display: inline-flex; align-items: center; margin-top: 30px; color: var(--brand); text-decoration: none; font-weight: bold; font-size: 1.1em; }}
            .back-btn:hover {{ gap: 10px; }}
            .back-btn span {{ margin-right: 8px; font-size: 1.2em; }}

            .main-footer {{ background: #1a1a1a; color: #ccc; padding: 60px 20px 0; margin-top: 80px; }}
            .footer-content {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 50px; padding-bottom: 40px; border-bottom: 1px solid #333; }}
            .footer-col h3, .footer-col h4 {{ color: white; margin-top: 0; margin-bottom: 20px; }}
            .footer-logo {{ font-size: 1.8em; color: var(--brand); font-weight: bold; }}
            .footer-desc {{ font-size: 0.95em; line-height: 1.6; color: #aaa; }}
            .footer-links a, .footer-contacts a {{ display: block; color: #ccc; text-decoration: none; margin-bottom: 10px; transition: color 0.2s; }}
            .footer-links a:hover, .footer-contacts a:hover {{ color: var(--brand); }}
            .contact-item {{ display: flex; align-items: center; gap: 10px; margin-bottom: 15px; color: #ccc; font-size: 0.95em; }}
            .contact-item svg {{ color: var(--brand); flex-shrink: 0; }}
            .contact-item a {{ color: #ccc; text-decoration: none; }}
            .social-links {{ display: flex; gap: 12px; margin-top: 20px; }}
            .social-link {{ display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; background: #333; border-radius: 50%; color: white; transition: all 0.3s; }}
            .social-link:hover {{ background: var(--brand); transform: translateY(-3px); }}
            .footer-bottom {{ max-width: 1200px; margin: 0 auto; padding: 25px 0; text-align: center; color: #777; font-size: 0.9em; }}

            @media (max-width: 768px) {{
                .main-header {{ padding: 10px 0; }}
                .header-inner {{ flex-direction: column; gap: 10px; padding: 10px 15px; }}
                .logo-area {{ width: 100%; justify-content: center; }}
                .logo-img {{ height: 50px !important; }}
                nav {{ flex-direction: row; flex-wrap: wrap; width: 100%; gap: 5px; justify-content: center; }}
                nav a {{ font-size: 0.85em; padding: 5px 8px; text-align: center; white-space: nowrap; }}
                .language-switcher {{ margin-left: 0 !important; padding-left: 0 !important; border-left: none !important; justify-content: center; width: 100%; margin-top: 5px; gap: 5px; }}
                .lang-link {{ font-size: 0.8em; padding: 4px 8px; }}
                .map-hero {{ padding: 160px 15px 40px; }}
                .map-hero h1 {{ font-size: 1.8em !important; }}
                .map-container {{ padding: 0 15px; margin-top: -20px; }}
                #map {{ height: 400px; }}
                .footer-content {{ grid-template-columns: 1fr; gap: 30px; text-align: center; }}
                .social-links, .contact-item {{ justify-content: center; }}
            }}
        </style>
    </head>
    <body>
        <header class="main-header">
            <div class="header-inner">
                <div class="logo-area"><a href="/" class="logo-link"><img src="/static/logo.png" alt="Logo" class="logo-img"></a></div>
                <nav>{nav_links}{lang_switcher}</nav>
            </div>
        </header>

        <div class="map-hero">
            <h1>{t['map_title']}</h1>
        </div>

        <div class="map-container">
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="total-trees">4690</div>
                    <div class="stat-label">Деревьев посажено</div>
                </div>
            </div>

            <div class="map-wrapper" style="margin-top: 30px;">
                <div id="map"></div>
            </div>

            <div class="legend">
                <h3>Условные обозначения</h3>
                <div class="legend-item">
                    <div class="legend-color stage1"></div>
                    <span>1-й этап — уже озеленен</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color stage2"></div>
                    <span>2-й этап — планируется</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color stage3"></div>
                    <span>3-й этап — планируется</span>
                </div>
            </div>

            <div style="text-align: center;">
                <a href="/" class="back-btn"><span>←</span> {t['back_home']}</a>
            </div>
        </div>

        {footer_html}

        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script>
            var map = L.map('map').setView([40.605, 43.963], 14);

            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/light_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: 'abcd',
                maxZoom: 20
            }}).addTo(map);

            var stages = {stages_json_str};

            // Цвета для каждого этапа (по индексу)
            var stageColors = [
                {{ color: '#2ecc71', borderColor: '#27ae60' }},  // 1-й этап - зеленый
                {{ color: '#f39c12', borderColor: '#e67e22' }},  // 2-й этап - оранжевый
                {{ color: '#e74c3c', borderColor: '#c0392b' }}   // 3-й этап - красный
            ];

            stages.forEach(function(stage, index) {{
                var isPlanted = stage.status === 'planted';
                var colors = stageColors[index];  // Используем индекс массива

                // Создаем полигоны для каждого этапа
                stage.polygons.forEach(function(polygonCoords) {{
                    var polygon = L.polygon(polygonCoords, {{
                        color: colors.borderColor,
                        weight: 3,
                        fillColor: colors.color,
                        fillOpacity: 0.5
                    }}).addTo(map);

                    // Popup с информацией
                    var statusText = isPlanted ? '✅ Озеленен' : '⏳ Планируется';
                    var treesInfo = stage.trees > 0 ? `<p style="margin: 5px 0;"><strong>Деревьев:</strong> ${{stage.trees.toLocaleString()}}</p>` : '';
                    
                    var popupContent = `
                        <div style="min-width: 220px;">
                            <h3 style="margin: 0 0 10px 0; color: #0F7874;">${{stage.name}}</h3>
                            <p style="margin: 5px 0;"><strong>Год:</strong> ${{stage.year}}</p>
                            <p style="margin: 5px 0;"><strong>Площадь:</strong> ${{stage.hectares}} га</p>
                            ${{treesInfo}}
                            <p style="margin: 5px 0;">${{stage.description}}</p>
                            <p style="margin: 10px 0 0 0; color: ${{colors.color}}; font-weight: bold;">
                                ${{statusText}}
                            </p>
                        </div>
                    `;

                    polygon.bindPopup(popupContent);

                    // Подсветка при наведении
                    polygon.on('mouseover', function(e) {{
                        this.setStyle({{ fillOpacity: 0.7, weight: 5 }});
                    }});
                    polygon.on('mouseout', function(e) {{
                        this.setStyle({{ fillOpacity: 0.5, weight: 3 }});
                    }});
                }});
            }});

            // Автоматически подгоняем карту под все участки
            if (stages.length > 0) {{
                var group = new L.featureGroup();
                stages.forEach(function(stage) {{
                    stage.polygons.forEach(function(coords) {{
                        group.addLayer(L.polygon(coords));
                    }});
                }});
                map.fitBounds(group.getBounds(), {{ padding: [50, 50] }});
            }}
        </script>
    </body>
    </html>
    """
    response = HttpResponse(html)
    response.set_cookie('django_language', lang, max_age=31536000)
    return response