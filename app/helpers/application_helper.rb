module ApplicationHelper
  def link_to_remove_fields(name, f)
    f.hidden_field(:_destroy) + link_to(name, '#', 'class' => 'removeFields')
  end

  def link_to_add_fields(name, f, association)
    new_object = f.object.class.reflect_on_association(association).klass.new
    fields = f.fields_for(association, new_object, :child_index => "new_#{association}") do |builder|
      render(association.to_s.singularize + "_fields", :f => builder)
    end
    add_field_template association, fields

    link_to name, '#',
            'data-association' => association,
            'class' => 'addFields'
  end

  def render_field_templates()
    result = ''

    if @field_template
      result << '<div class=\'fieldTemplates\'>'

      @field_template.each {|key, value|
        result << "<div data-template-for='#{key}'>"
        result << value
        result << '</div>'
      }

      result << '</div>'
    end

    result.html_safe
  end

  private

  def add_field_template(name, template)
    unless @field_template
      @field_template = {}
    end

    @field_template[name] = template
  end
end
