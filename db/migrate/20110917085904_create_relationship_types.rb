class CreateRelationshipTypes < ActiveRecord::Migration
  def change
    create_table :relationship_types do |t|
      t.string :name
      t.text :description

      t.timestamps
    end
  end
end
