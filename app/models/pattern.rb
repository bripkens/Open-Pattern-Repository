class Pattern < ActiveRecord::Base
  has_many :outgoing_relationships, :foreign_key => 'source_id',
           :class_name => 'PatternRelationship', :dependent => :destroy
  has_many :incoming_relationships, :foreign_key => 'target_id',
           :class_name => 'PatternRelationship', :dependent => :destroy

  accepts_nested_attributes_for :outgoing_relationships,
                                :allow_destroy => true

  acts_as_taggable

  def to_param
    slug
  end

  validates :name, :slug, :uniqueness => {:case_sensitive => false}
  validates :name, :description, :slug, :presence => true
  validates :description, :length => {:minimum => 10}
  validates :slug, :format => {
      :with => %r{^[a-z0-9_-]+$}i,
      :message => 'must only consist of alphanumeric characters, underscores or
                   dashes'
  }
end
