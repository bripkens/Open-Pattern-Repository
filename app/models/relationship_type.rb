class RelationshipType < ActiveRecord::Base
  default_scope :order => 'name'
  has_many :pattern_relationships
  validates :name, :presence => true, :uniqueness => {:case_sensitive => false}
end
