class WelcomeController < ApplicationController
  def index
    @page_title = 'Welcome'
    @latest_patterns = Pattern.find(:all,
                                    :limit => 3,
                                    :order => 'created_at desc')
  end
end
