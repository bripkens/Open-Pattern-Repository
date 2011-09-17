module LayoutHelper
  def title(page_title)
    content_for(:title) { h(page_title.to_s) }
  end

  def set_active_page(page_title)
    @active_page = page_title
  end

  def active_page?(page_title)
    @active_page == page_title ? 'active' : ''
  end
end