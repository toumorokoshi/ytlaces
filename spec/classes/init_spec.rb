require 'spec_helper'
describe 'laces' do
  context 'with default values for all parameters' do
    it { should contain_class('laces') }
  end
end
