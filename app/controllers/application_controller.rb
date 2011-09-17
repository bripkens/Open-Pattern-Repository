class ApplicationController < ActionController::Base
  protect_from_forgery
  #before_filter :require_authorization, :require_editor, :require_admin
  helper_method :current_user, :authorized?, :admin?, :editor?

  private

  def authorized?
    return true if current_user else false
  end

  def admin?
    true
    #authorized? && @current_user.admin?
  end

  def editor?
    authorized? && @current_user.editor?
  end

  def current_user
    @current_user ||= User.find(session[:user_id]) if session[:user_id]
  end

  def require_authorization
    unless authorized?
      redirect_to root_url, :notice => 'Access is restricted to authorized users.'
    end
  end

  def require_editor
    unless editor?
      redirect_to root_url, :notice => 'Access is restricted to editors.'
    end
  end

  def require_admin
    unless admin?
      redirect_to root_url, :notice => 'Access is restricted to administrators.'
    end
  end

end
