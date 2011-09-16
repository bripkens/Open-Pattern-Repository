require 'test_helper'

class PatternsControllerTest < ActionController::TestCase
  setup do
    @pattern = patterns(:one)
  end

  test "should get index" do
    get :index
    assert_response :success
    assert_not_nil assigns(:patterns)
  end

  test "should get new" do
    get :new
    assert_response :success
  end

  test "should create pattern" do
    assert_difference('Pattern.count') do
      post :create, :pattern => @pattern.attributes
    end

    assert_redirected_to pattern_path(assigns(:pattern))
  end

  test "should show pattern" do
    get :show, :id => @pattern.to_param
    assert_response :success
  end

  test "should get edit" do
    get :edit, :id => @pattern.to_param
    assert_response :success
  end

  test "should update pattern" do
    put :update, :id => @pattern.to_param, :pattern => @pattern.attributes
    assert_redirected_to pattern_path(assigns(:pattern))
  end

  test "should destroy pattern" do
    assert_difference('Pattern.count', -1) do
      delete :destroy, :id => @pattern.to_param
    end

    assert_redirected_to patterns_path
  end
end
